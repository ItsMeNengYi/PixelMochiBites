"""
Playwright + Gemini Browser Automation - Web Interface (Fixed)
A browser extension-like overlay that sits on top of any webpage
"""

import os
import json
import asyncio
from flask import Flask, request, jsonify, make_response
from threading import Thread
from playwright.async_api import async_playwright
import google.generativeai as genai
from flask_cors import CORS  

from dotenv import load_dotenv
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=GEMINI_API_KEY)

app = Flask(__name__)

CORS(app, resources={r"/*": {"origins": "*"}})

class BrowserController:
    def __init__(self):
        self.page = None
        self.browser = None
        self.context = None
        self.model = genai.GenerativeModel("gemini-3-flash-preview")
        self.loop = None
        self.original_html = {}
        self.playwright_instance = None
        
    async def start_browser(self):
        print("Starting browser...")
        self.playwright_instance = await async_playwright().start()
        
        # Add these specific flags to bypass security restrictions
        self.browser = await self.playwright_instance.chromium.launch(
            headless=False,
            args=[
                "--disable-web-security",
                "--allow-running-insecure-content"
            ]
        )
        
        # Also tell the context to ignore HTTPS errors
        self.context = await self.browser.new_context(ignore_https_errors=True)
        self.page = await self.context.new_page()
        
        # Set up event listener for page loads
        self.page.on("load", lambda: asyncio.create_task(self._on_page_load()))
        
        print("Browser started successfully")
        
    async def _on_page_load(self):
        """Called when page loads"""
        try:
            await asyncio.sleep(0.3)
            await self._inject_overlay()
        except Exception as e:
            print(f"Error on page load: {e}")
        
    async def _inject_overlay(self):
        """Inject the control panel overlay into the page"""
        try:
            overlay_script = """
            (function() {
                const existing = document.getElementById('ai-control-overlay');
                if (existing) existing.remove();
                
                const overlay = document.createElement('div');
                overlay.id = 'ai-control-overlay';
                overlay.innerHTML = `
                    <div style="position: fixed; top: 10px; right: 10px; width: 350px;
                        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                        border-radius: 12px; box-shadow: 0 10px 40px rgba(0,0,0,0.3);
                        z-index: 999999; font-family: -apple-system, sans-serif; color: white;">
                        <div style="padding: 15px; border-bottom: 1px solid rgba(255,255,255,0.2);">
                            <div style="display: flex; justify-content: space-between; align-items: center;">
                                <h3 style="margin: 0; font-size: 16px; font-weight: 600;">🤖 AI Browser Control</h3>
                                <button onclick="document.getElementById('ai-control-overlay').style.display='none'" 
                                    style="background: rgba(255,255,255,0.2); border: none; color: white; 
                                           padding: 5px 10px; border-radius: 6px; cursor: pointer; font-size: 12px;">
                                    Hide
                                </button>
                            </div>
                        </div>
                        <div style="padding: 15px;">
                            <input type="text" id="ai-command-input" placeholder="Type your command..." 
                                style="width: 100%; padding: 10px; border: none; border-radius: 8px; 
                                       font-size: 14px; box-sizing: border-box; 
                                       background: rgba(255,255,255,0.9); color: #333;">
                            <button onclick="executeCommand()" 
                                style="width: 100%; margin-top: 10px; padding: 10px; 
                                       background: rgba(255,255,255,0.2); border: none; 
                                       color: white; border-radius: 8px; cursor: pointer; 
                                       font-weight: 600; font-size: 14px;">
                                Execute
                            </button>
                            <div style="margin-top: 15px; display: grid; grid-template-columns: 1fr 1fr; gap: 8px;">
                                <button onclick="executeQuick('scroll down')" class="quick-btn">⬇️ Scroll Down</button>
                                <button onclick="executeQuick('scroll up')" class="quick-btn">⬆️ Scroll Up</button>
                                <button onclick="executeQuick('go back')" class="quick-btn">⬅️ Go Back</button>
                                <button onclick="simplifyPage()" class="quick-btn">✨ Simplify</button>
                            </div>
                            <div id="ai-status" style="margin-top: 10px; padding: 8px; 
                                background: rgba(0,0,0,0.2); border-radius: 6px; 
                                font-size: 12px; min-height: 40px; display: none;">
                            </div>
                        </div>
                    </div>
                    <style>
                        .quick-btn {
                            padding: 8px; background: rgba(255,255,255,0.15);
                            border: none; color: white; border-radius: 6px;
                            cursor: pointer; font-size: 12px; transition: all 0.2s;
                        }
                        .quick-btn:hover {
                            background: rgba(255,255,255,0.25);
                            transform: translateY(-2px);
                        }
                    </style>
                `;
                
                document.body.appendChild(overlay);
                document.getElementById('ai-command-input').addEventListener('keypress', function(e) {
                    if (e.key === 'Enter') executeCommand();
                });
                
                window.executeCommand = async function() {
                    const input = document.getElementById('ai-command-input');
                    const command = input.value.trim();
                    if (!command) return;
                    showStatus('⚙️ Processing...');
                    try {
                        const response = await fetch('http://127.0.0.1:5000/execute', { // Use 127.0.0.1 instead of localhost
                            method: 'POST',
                            headers: {'Content-Type': 'application/json'},
                            body: JSON.stringify({command: command})
                        });
                        
                        // Safety check: Don't parse if response is empty
                        const text = await response.text();
                        const result = text ? JSON.parse(text) : { success: false, message: 'Empty response' };
                        
                        showStatus(result.success ? '✅ ' + result.message : '❌ ' + result.message);
                        if (result.success) input.value = '';
                    } catch (error) {
                        showStatus('❌ Error: ' + error.message);
                    }
                };
                
                window.executeQuick = function(command) {
                    document.getElementById('ai-command-input').value = command;
                    executeCommand();
                };
                
                window.simplifyPage = async function() {
                    showStatus('✨ Simplifying page...');
                    try {
                        const response = await fetch('http://localhost:5000/simplify', {method: 'POST'});
                        const result = await response.json();
                        showStatus(result.success ? '✅ Page simplified!' : '❌ ' + result.message);
                    } catch (error) {
                        showStatus('❌ Error: ' + error.message);
                    }
                };
                
                window.showStatus = function(message) {
                    const status = document.getElementById('ai-status');
                    status.style.display = 'block';
                    status.textContent = message;
                    setTimeout(() => { status.style.display = 'none'; }, 5000);
                };
            })();
            """
            
            await self.page.evaluate(overlay_script)
            print("✓ Overlay injected")
        except Exception as e:
            print(f"✗ Error injecting overlay: {e}")
        
    async def save_original_html(self):
        """Save the original HTML before simplification"""
        try:
            url = self.page.url
            html = await self.page.content()
            self.original_html[url] = html
            print(f"✓ Saved original HTML for {url}")
            return True
        except Exception as e:
            print(f"✗ Error saving HTML: {e}")
            return False
        
    async def restore_original_html(self):
        """Restore the original HTML"""
        try:
            url = self.page.url
            if url in self.original_html:
                await self.page.set_content(self.original_html[url])
                await self._inject_overlay()
                print(f"✓ Restored original HTML for {url}")
                return True
            print(f"✗ No original HTML saved for {url}")
            return False
        except Exception as e:
            print(f"✗ Error restoring HTML: {e}")
            return False
        
    async def simplify_page(self):
        """Simplify page for cognitive impaired users"""
        await self.save_original_html()
        
        simplify_script = """
        (function() {
            const selectorsToRemove = [
                'iframe:not([id*="ai-control"])', 'video:not([controls])', 'aside',
                'nav:not(.main-nav)', '.advertisement', '.ad', '.popup', '.modal',
                '.sidebar', '[class*="banner"]', '[class*="cookie"]', '[class*="social"]'
            ];
            selectorsToRemove.forEach(selector => {
                try {
                    document.querySelectorAll(selector).forEach(el => el.remove());
                } catch(e) {}
            });
            
            const styleSheet = document.createElement('style');
            styleSheet.textContent = `
                * { animation: none !important; transition: none !important; }
                body {
                    font-family: -apple-system, sans-serif !important;
                    line-height: 1.8 !important; font-size: 18px !important;
                    max-width: 900px !important; margin: 0 auto !important;
                    padding: 40px 20px !important; background: #fff !important;
                    color: #333 !important;
                }
                h1, h2, h3 { font-weight: 700 !important; color: #000 !important; }
                h1 { font-size: 32px !important; }
                h2 { font-size: 26px !important; }
                p { margin-bottom: 1.2em !important; }
                a { color: #0066cc !important; text-decoration: underline !important; font-weight: 600 !important; }
                button { background: #0066cc !important; color: white !important; padding: 12px 20px !important; }
            `;
            document.head.appendChild(styleSheet);
            
            const restoreBtn = document.createElement('div');
            restoreBtn.innerHTML = `
                <button onclick="restoreOriginal()" style="
                    position: fixed !important; bottom: 20px !important; right: 20px !important;
                    background: #ff6b6b !important; color: white !important;
                    padding: 12px 24px !important; border: none !important;
                    border-radius: 8px !important; cursor: pointer !important;
                    z-index: 999998 !important; box-shadow: 0 4px 12px rgba(0,0,0,0.2) !important;">
                    🔄 Restore Original
                </button>
            `;
            document.body.appendChild(restoreBtn);
            
            window.restoreOriginal = async function() {
                const response = await fetch('http://localhost:5000/restore', {method: 'POST'});
                const result = await response.json();
                if (result.success) location.reload();
            };
            
            return {simplified: true};
        })();
        """
        
        try:
            result = await self.page.evaluate(simplify_script)
            print("✓ Page simplified")
            return result.get('simplified', False)
        except Exception as e:
            print(f"✗ Error simplifying page: {e}")
            return False
        
    async def get_page_context(self):
        """Get current page information"""
        try:
            url = self.page.url
            title = await self.page.title()
            buttons = await self.page.evaluate("""() => {
                const buttons = Array.from(document.querySelectorAll('button, a, input[type="submit"]'));
                return buttons.slice(0, 20).map(btn => ({
                    text: btn.innerText || btn.value || btn.getAttribute('aria-label') || '',
                    type: btn.tagName
                }));
            }""")
            inputs = await self.page.evaluate("""() => {
                const inputs = Array.from(document.querySelectorAll('input:not([type="submit"]), textarea'));
                return inputs.slice(0, 15).map(inp => ({
                    type: inp.type, placeholder: inp.placeholder, name: inp.name
                }));
            }""")
            return {"url": url, "title": title, "buttons": buttons, "inputs": inputs}
        except Exception as e:
            print(f"✗ Error getting page context: {e}")
            return {"error": str(e)}
            
    async def send_to_gemini(self, command, context):
        """Send command to Gemini for interpretation"""
        prompt = f"""You are a browser automation assistant. Convert this command to actions.

Current Page: {context.get('url', 'N/A')}
Available Buttons: {json.dumps(context.get('buttons', [])[:10])}
Available Inputs: {json.dumps(context.get('inputs', [])[:10])}

User Command: {command}

Respond with JSON array only:
[
    {{"action": "click|type|navigate|scroll|wait", "selector": "...", "value": "...", "description": "..."}}
]

Actions: click, type (needs value), navigate (needs URL in value), scroll (value: up/down), wait (value: ms)
"""
        try:
            response = self.model.generate_content(prompt)
            print(response)
            text = response.text.strip()
            if text.startswith("```"): text = "\n".join(text.split("\n")[1:-1])
            if text.startswith("```json"): text = text[7:]
            if text.endswith("```"): text = text[:-3]
            return json.loads(text.strip())
        except Exception as e:
            print(f"✗ Gemini error: {e}")
            return [{"action": "error", "description": str(e)}]
            
    async def execute_actions(self, actions):
        """Execute actions from Gemini"""
        for i, action in enumerate(actions, 1):
            act = action.get("action")
            sel = action.get("selector")
            val = action.get("value")
            desc = action.get("description", "")
            print(f"[{i}] {desc}")
            try:
                if act == "error":
                    print(f"✗ {desc}")
                    return False
                elif act == "navigate":
                    await self.page.goto(val)
                    await self.page.wait_for_load_state("networkidle")
                elif act == "click":
                    try:
                        await self.page.click(sel, timeout=5000)
                    except:
                        await self.page.get_by_text(sel).first.click(timeout=5000)
                elif act == "type":
                    await self.page.fill(sel, val)
                elif act == "wait":
                    await asyncio.sleep(int(val) / 1000)
                elif act == "scroll":
                    pixels = 500 if val.lower() == "down" else -500
                    await self.page.evaluate(f"window.scrollBy(0, {pixels})")
                await asyncio.sleep(0.5)
            except Exception as e:
                print(f"✗ Error executing {act}: {e}")
                return False
        print("✓ All actions completed")
        return True
        
    async def close(self):
        if self.browser:
            await self.browser.close()
        if self.playwright_instance:
            await self.playwright_instance.stop()

controller = BrowserController()

@app.before_request
def handle_preflight():
    if request.method == "OPTIONS":
        response = make_response()
        response.headers.add("Access-Control-Allow-Origin", "*")
        response.headers.add('Access-Control-Allow-Headers', "*")
        response.headers.add('Access-Control-Allow-Methods', "*")
        return response

@app.route('/')
def index():
    return '''<!DOCTYPE html>
    <html><head><title>AI Browser Control</title><style>
        body { font-family: -apple-system, sans-serif; margin: 0; padding: 20px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh; display: flex; justify-content: center; align-items: center; }
        .container { background: white; padding: 40px; border-radius: 16px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3); max-width: 500px; width: 100%; }
        h1 { margin: 0 0 10px 0; color: #333; }
        p { color: #666; margin-bottom: 30px; }
        button { width: 100%; padding: 15px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white; border: none; border-radius: 8px; font-size: 16px; font-weight: 600;
            cursor: pointer; transition: transform 0.2s; }
        button:hover:not(:disabled) { transform: translateY(-2px); }
        button:disabled { opacity: 0.6; cursor: not-allowed; }
        #status { margin-top: 20px; padding: 15px; background: #f0f0f0; border-radius: 8px; display: none; }
    </style></head><body>
        <div class="container">
            <h1>🤖 AI Browser Control</h1>
            <p>Click the button below to start the browser with the AI control overlay</p>
            <button id="startBtn" onclick="startBrowser()">Start Browser</button>
            <div id="status"></div>
        </div>
        <script>
            async function startBrowser() {
                const btn = document.getElementById('startBtn');
                const status = document.getElementById('status');
                btn.disabled = true; btn.textContent = 'Starting browser...';
                status.style.display = 'block'; status.textContent = '⚙️ Launching browser...';
                try {
                    const response = await fetch('/start', {method: 'POST'});
                    const result = await response.json();
                    if (result.success) {
                        status.textContent = '✅ Browser started! Look for the control overlay in the top-right corner.';
                        btn.textContent = 'Browser Running';
                    } else {
                        status.textContent = '❌ ' + result.message;
                        btn.disabled = false; btn.textContent = 'Start Browser';
                    }
                } catch (error) {
                    status.textContent = '❌ Error: ' + error.message;
                    btn.disabled = false; btn.textContent = 'Start Browser';
                }
            }
        </script>
    </body></html>'''

@app.route('/start', methods=['POST'])
def start_browser():
    try:
        if not controller.loop:
            controller.loop = asyncio.new_event_loop()
            def run_loop():
                asyncio.set_event_loop(controller.loop)
                controller.loop.run_until_complete(controller.start_browser())
                controller.loop.run_until_complete(controller.page.goto("https://www.google.com"))
                controller.loop.run_forever()
            thread = Thread(target=run_loop, daemon=True)
            thread.start()
            import time
            time.sleep(2)
            return jsonify({"success": True, "message": "Browser started"})
        else:
            return jsonify({"success": True, "message": "Browser already running"})
    except Exception as e:
        return jsonify({"success": False, "message": str(e)})

@app.route('/execute', methods=['POST'])
def execute_command():
    try:
        data = request.json
        command = data.get('command', '')
        print(f"\n> Command: {command}")
        async def run_command():
            context = await controller.get_page_context()
            actions = await controller.send_to_gemini(command, context)
            success = await controller.execute_actions(actions)
            return success
        future = asyncio.run_coroutine_threadsafe(run_command(), controller.loop)
        success = future.result(timeout=30)
        return jsonify({"success": success, "message": "Command executed" if success else "Command failed"})
    except Exception as e:
        print(f"✗ Error: {e}")
        return jsonify({"success": False, "message": str(e)})

@app.route('/simplify', methods=['POST'])
def simplify_page():
    try:
        async def run_simplify():
            return await controller.simplify_page()
        future = asyncio.run_coroutine_threadsafe(run_simplify(), controller.loop)
        success = future.result(timeout=10)
        return jsonify({"success": success, "message": "Page simplified" if success else "Failed to simplify"})
    except Exception as e:
        print(f"✗ Error: {e}")
        return jsonify({"success": False, "message": str(e)})

@app.route('/restore', methods=['POST'])
def restore_page():
    try:
        async def run_restore():
            return await controller.restore_original_html()
        future = asyncio.run_coroutine_threadsafe(run_restore(), controller.loop)
        success = future.result(timeout=10)
        return jsonify({"success": success, "message": "Page restored" if success else "No original to restore"})
    except Exception as e:
        print(f"✗ Error: {e}")
        return jsonify({"success": False, "message": str(e)})

if __name__ == '__main__':
    print("\n" + "="*60)
    print("🤖 AI Browser Control - Web Interface")
    print("="*60)
    print("\n➡️  Open http://localhost:5000 in your browser")
    print("="*60 + "\n")
    app.run(debug=False, host='127.0.0.1', port=5000, use_reloader=False)