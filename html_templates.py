"""
HTML Templates Module
Contains all HTML, CSS, and JavaScript for overlay and landing page
"""

def get_overlay_script():
    """Returns the JavaScript code to inject the AI control overlay"""
    return """
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
                const response = await fetch('http://127.0.0.1:5000/execute', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({command: command})
                });
                
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
            setTimeout(() => status.style.display = 'none', 3000);
        };
    })();
    """

def get_landing_page_html():
    """Returns the HTML for the landing page"""
    return '''<!DOCTYPE html>
    <html>
    <head>
        <title>AI Browser Control</title>
        <style>
            body { 
                font-family: -apple-system, sans-serif; 
                margin: 0; 
                padding: 20px;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh; 
                display: flex; 
                justify-content: center; 
                align-items: center; 
            }
            .container { 
                background: white; 
                padding: 40px; 
                border-radius: 16px;
                box-shadow: 0 20px 60px rgba(0,0,0,0.3); 
                max-width: 500px; 
                width: 100%; 
            }
            h1 { 
                margin: 0 0 10px 0; 
                color: #333; 
            }
            p { 
                color: #666; 
                margin-bottom: 30px; 
            }
            button { 
                width: 100%; 
                padding: 15px; 
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white; 
                border: none; 
                border-radius: 8px; 
                font-size: 16px; 
                font-weight: 600;
                cursor: pointer; 
                transition: transform 0.2s; 
            }
            button:hover:not(:disabled) { 
                transform: translateY(-2px); 
            }
            button:disabled { 
                opacity: 0.6; 
                cursor: not-allowed; 
            }
            #status { 
                margin-top: 20px; 
                padding: 15px; 
                background: #f0f0f0; 
                border-radius: 8px; 
                display: none; 
            }
        </style>
    </head>
    <body>
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
                btn.disabled = true; 
                btn.textContent = 'Starting browser...';
                status.style.display = 'block'; 
                status.textContent = '⚙️ Launching browser...';
                
                try {
                    const response = await fetch('/start', {method: 'POST'});
                    const result = await response.json();
                    
                    if (result.success) {
                        status.textContent = '✅ Browser started! Look for the control overlay in the top-right corner.';
                        btn.textContent = 'Browser Running';
                    } else {
                        status.textContent = '❌ ' + result.message;
                        btn.disabled = false; 
                        btn.textContent = 'Start Browser';
                    }
                } catch (error) {
                    status.textContent = '❌ Error: ' + error.message;
                    btn.disabled = false; 
                    btn.textContent = 'Start Browser';
                }
            }
        </script>
    </body>
    </html>'''