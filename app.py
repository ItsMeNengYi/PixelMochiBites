"""
Flask Application - Main Entry Point
Handles all HTTP routes and coordinates with BrowserController
"""

import asyncio
import time
from threading import Thread
from flask import Flask, request, jsonify, make_response, redirect, url_for
from flask_cors import CORS

from config import Config
from browser_controller import BrowserController
from ai_agent import AIAgent
from web_manager import WebManager
from html_templates import get_landing_page_html, get_select_interact_page_html, get_browser_page_html
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
voice_agent = VoiceAssistant()
ai_agent = AIAgent()
web_manager = WebManager()
controller = BrowserController(ai_agent=ai_agent, web_manager=web_manager)

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
    return get_landing_page_html()

@app.route('/input_selection')
def input_selection():
    return get_select_interact_page_html()

@app.route('/browser')
def browser():
    return get_browser_page_html()

@app.route('/get_current_state')
def get_current_state():
    # Simply tell the browser which page it SHOULD be on
    return jsonify({"current_page": Config.PAGE})

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
def speak_action():
    text = request.args.get('text', '')
    print(f"→ Speaking: {text}")
    voice_agent.speak(text)
    return jsonify(success=True)

@app.route('/button_select', methods=['POST'])
def select_route():
    text = request.args.get('text', '')
    voice_agent.speak("Focus " + text)
    return jsonify(success=True)

@app.route('/button_click', methods=['POST'])
def click_route():
    """Handle button clicks and process navigation"""
    text = request.args.get('text', '')
    print(f"Button click received: {text}")
    
    # Process the navigation in a background thread
    thread = Thread(target=lambda: process_navigation(text, voice=False), daemon=True)
    thread.start()
    
    return jsonify({"success": True})

def voice_callback(text):
    """Callback for voice recognition"""
    command = text
    print(f"→ Recognized command: {command}")
    if command:
        process_navigation(command, voice=True)
        
async def handle_browse_async(cmd):
    """Async version of handle_browse"""
    # Let the AI interpret the command
    nav_data = await ai_agent.navigate_url(cmd)
    
    voice_agent.speak(nav_data['description'])
    
    if not nav_data['url']:
        return
    
    url = nav_data['url']
    
    # Check if browser page is ready
    if controller.web_manager.page is not None:
        # Navigate to new URL
        await controller.navigate_to(url)
        return
    
    # Start new browser and navigate
    await controller.start_browser()
    await controller.navigate_to(url)

def process_navigation(command, voice=False):
    """Centralized logic for both voice and button inputs."""
    print(f"→ Processing navigation command: {command} (voice={voice})")

    current_page = Config.PAGE
    
    # Handle browsing mode
    if current_page == "/browser":
        # Check if event loop exists and is running
        if controller.web_manager.loop is not None and controller.web_manager.loop.is_running():
            # Browser loop already running, just navigate
            print("→ Using existing browser event loop")
            future = asyncio.run_coroutine_threadsafe(
                handle_browse_async(command),
                controller.web_manager.loop
            )
            try:
                future.result(timeout=15)
            except Exception as e:
                print(f"ERROR [process_navigation]: Navigation failed - {str(e)}")
                voice_agent.speak("Failed to navigate")
        else:
            # Need to create new event loop and start browser
            print("→ Creating new browser event loop")
            controller.web_manager.loop = asyncio.new_event_loop()
            
            def run_loop():
                """Run the async event loop in a separate thread"""
                try:
                    asyncio.set_event_loop(controller.web_manager.loop)
                    # Run the browse handler and then keep loop alive
                    controller.web_manager.loop.run_until_complete(handle_browse_async(command))
                    print("✓ Browser initialized and navigated")
                    # Keep loop running for future commands
                    controller.web_manager.loop.run_forever()
                except Exception as e:
                    print(f"ERROR [app.run_loop]: Event loop failed - {str(e)}")
                    voice_agent.speak("Failed to start browser")
                finally:
                    # Cleanup
                    try:
                        if controller.web_manager.loop.is_running():
                            controller.web_manager.loop.close()
                    except:
                        pass
            
            # Start browser in background thread
            thread = Thread(target=run_loop, daemon=True)
            thread.start()
            
            # Wait for browser to initialize
            print("→ Waiting for browser to initialize...")
            time.sleep(3)
        return
    
    # Parse commands
    if voice:
        cmds = command.split(" ")
    else:
        cmds = [command]
    
    for command in cmds:
        cmd = command.lower().strip()
        
        # Global 'Back' Logic
        if "back" in cmd:
            Config.previous_page()
            voice_agent.speak("Going back")
            return

        # Page-Specific Logic
        if current_page == "/":
            if cmd in ['see', 'hear', 'both']:
                Config.set_setting('INTERACTION_MODE', cmd)
                if cmd == 'see':
                    voice_agent.mute()
                else:
                    voice_agent.unmute()
                voice_agent.speak(f"Selected {cmd}")
                time.sleep(1)
                Config.next_page()
                return
                
        elif current_page == "/input_selection":
            if cmd in ['keyboard', 'speech']:
                Config.set_setting('INPUT_MODE', cmd)
                if cmd == "keyboard":
                    voice_agent.mute_mic()
                else:
                    voice_agent.unmute_mic()
                voice_agent.speak(f"Selected {cmd}")
                time.sleep(1)
                Config.next_page()
                return

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
    
    voice_agent.start_non_blocking_listen(callback=voice_callback)
    app.run(
        debug=Config.FLASK_DEBUG,
        host=Config.FLASK_HOST,
        port=Config.FLASK_PORT,
        use_reloader=False
    )

if __name__ == '__main__':
    main()