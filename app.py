"""
Flask Application - Main Entry Point
Handles all HTTP routes and coordinates with BrowserController
"""

import asyncio
import time
from threading import Thread
from flask import Flask, request, jsonify, make_response
from flask_cors import CORS

from config import Config
from browser_controller import BrowserController
from html_templates import get_landing_page_html
from voice_agent import VoiceAssistant

# Validate configuration
try:
    Config.validate()
except Exception as e:
    print(f"\n{str(e)}")
    print("Please set GEMINI_API_KEY in your .env file\n")
    exit(1)

# Initialize Flask app
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

# Initialize agents
controller = BrowserController()
voice_agent = VoiceAssistant()

@app.before_request
def handle_preflight():
    """Handle CORS preflight requests"""
    if request.method == "OPTIONS":
        response = make_response()
        response.headers.add("Access-Control-Allow-Origin", "*")
        response.headers.add('Access-Control-Allow-Headers', "*")
        response.headers.add('Access-Control-Allow-Methods', "*")
        return response

@app.route('/')
def index():
    """Landing page route"""
    try:
        return get_landing_page_html()
    except Exception as e:
        print(f"ERROR [app.index]: Failed to load landing page - {str(e)}")
        return jsonify({"error": "Failed to load page"}), 500

@app.route('/start', methods=['POST'])
def start_browser():
    """
    Start the browser instance
    
    Returns:
        JSON response with success status and message
    """
    try:
        # Check if browser is already running
        if controller.web_manager.loop and controller.web_manager.loop.is_running():
            return jsonify({
                "success": True, 
                "message": "Browser already running"
            })
        
        # Create new event loop for browser
        controller.web_manager.loop = asyncio.new_event_loop()
        
        def run_loop():
            """Run the async event loop in a separate thread"""
            try:
                asyncio.set_event_loop(controller.web_manager.loop)
                controller.web_manager.loop.run_until_complete(controller.start_browser())
                controller.web_manager.loop.run_until_complete(
                    controller.navigate_to("https://www.google.com")
                )
                controller.web_manager.loop.run_forever()
            except Exception as e:
                print(f"ERROR [app.start_browser.run_loop]: Event loop failed - {str(e)}")
        
        # Start browser in background thread
        thread = Thread(target=run_loop, daemon=True)
        thread.start()
        
        # Wait for browser to initialize
        time.sleep(2)
        
        return jsonify({
            "success": True, 
            "message": "Browser started"
        })
        
    except Exception as e:
        error_msg = f"ERROR [app.start_browser]: {str(e)}"
        print(error_msg)
        return jsonify({
            "success": False, 
            "message": str(e)
        }), 500

@app.route('/execute', methods=['POST'])
def execute_command():
    """
    Execute a natural language command
    
    Expected JSON body:
        {"command": "your command here"}
    
    Returns:
        JSON response with success status and message
    """
    try:
        # Parse request
        data = request.json
        if not data or 'command' not in data:
            return jsonify({
                "success": False,
                "message": "No command provided"
            }), 400
        
        command = data.get('command', '').strip()
        if not command:
            return jsonify({
                "success": False,
                "message": "Empty command"
            }), 400
        
        print(f"\n> Command received: {command}")
        
        # Execute command asynchronously
        async def run_command():
            return await controller.execute_command(command)
        
        future = asyncio.run_coroutine_threadsafe(
            run_command(), 
            controller.web_manager.loop
        )
        
        # Wait for completion with timeout
        success = future.result(timeout=Config.COMMAND_TIMEOUT)
        
        return jsonify({
            "success": success,
            "message": "Command executed" if success else "Command failed"
        })
        
    except asyncio.TimeoutError:
        error_msg = f"ERROR [app.execute_command]: Command timed out after {Config.COMMAND_TIMEOUT}s"
        print(error_msg)
        return jsonify({
            "success": False,
            "message": f"Command timed out"
        }), 408
        
    except Exception as e:
        error_msg = f"ERROR [app.execute_command]: {str(e)}"
        print(error_msg)
        return jsonify({
            "success": False,
            "message": str(e)
        }), 500

@app.route('/simplify', methods=['POST'])
def simplify_page():
    """
    Simplify the current page by removing clutter
    
    Returns:
        JSON response with success status and message
    """
    try:
        async def run_simplify():
            return await controller.simplify_page()
        
        future = asyncio.run_coroutine_threadsafe(
            run_simplify(), 
            controller.web_manager.loop
        )
        
        success = future.result(timeout=Config.SIMPLIFY_TIMEOUT)
        
        return jsonify({
            "success": success,
            "message": "Page simplified" if success else "Failed to simplify"
        })
        
    except asyncio.TimeoutError:
        error_msg = f"ERROR [app.simplify_page]: Simplify timed out after {Config.SIMPLIFY_TIMEOUT}s"
        print(error_msg)
        return jsonify({
            "success": False,
            "message": "Simplify timed out"
        }), 408
        
    except Exception as e:
        error_msg = f"ERROR [app.simplify_page]: {str(e)}"
        print(error_msg)
        return jsonify({
            "success": False,
            "message": str(e)
        }), 500

@app.route('/restore', methods=['POST'])
def restore_page():
    """
    Restore the page to its original state
    
    Returns:
        JSON response with success status and message
    """
    try:
        async def run_restore():
            return await controller.restore_page()
        
        future = asyncio.run_coroutine_threadsafe(
            run_restore(), 
            controller.web_manager.loop
        )
        
        success = future.result(timeout=Config.RESTORE_TIMEOUT)
        
        return jsonify({
            "success": success,
            "message": "Page restored" if success else "No original to restore"
        })
        
    except asyncio.TimeoutError:
        error_msg = f"ERROR [app.restore_page]: Restore timed out after {Config.RESTORE_TIMEOUT}s"
        print(error_msg)
        return jsonify({
            "success": False,
            "message": "Restore timed out"
        }), 408
        
    except Exception as e:
        error_msg = f"ERROR [app.restore_page]: {str(e)}"
        print(error_msg)
        return jsonify({
            "success": False,
            "message": str(e)
        }), 500
    
@app.route('/speak', methods=['POST'])
def speak_route():
    text = request.args.get('text', '')
    # Use speak_interrupt so it doesn't overlap if they tab quickly
    voice_agent.speak(text)
    return jsonify(success=True)

@app.route('/button_select', methods=['POST'])
def select_route():
    text = request.args.get('text', '')
    # Use speak_interrupt so it doesn't overlap if they tab quickly
    voice_agent.speak("Focus " + text)
    return jsonify(success=True)

@app.route('/button_click', methods=['POST'])
def click_route():
    text = request.args.get('text', '')
    # Use speak_interrupt so it doesn't overlap if they tab quickly
    voice_agent.speak("Selected " + text)
    return jsonify(success=True)

@app.errorhandler(404)
def not_found(e):
    """Handle 404 errors"""
    return jsonify({
        "success": False,
        "message": "Endpoint not found"
    }), 404

@app.errorhandler(500)
def internal_error(e):
    """Handle 500 errors"""
    error_msg = f"ERROR [app.internal_error]: Internal server error - {str(e)}"
    print(error_msg)
    return jsonify({
        "success": False,
        "message": "Internal server error"
    }), 500

def main():
    """Main entry point"""
    print("\n" + "="*60)
    print("🤖 AI Browser Control - Web Interface")
    print("="*60)
    print(f"\n➡️  Open http://{Config.FLASK_HOST}:{Config.FLASK_PORT} in your browser")
    print("="*60 + "\n")
    
    app.run(
        debug=Config.FLASK_DEBUG,
        host=Config.FLASK_HOST,
        port=Config.FLASK_PORT,
        use_reloader=False
    )

if __name__ == '__main__':
    main()