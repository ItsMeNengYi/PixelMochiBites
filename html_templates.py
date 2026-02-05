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
    <style>
        body {
            font-family: sans-serif;
            background-color: #FFFDE7; /* Soft yellow is easier on the eyes */
            display: flex;
            flex-direction: column;
            align-items: center;
            padding: 50px;
        }
        h1 { font-size: 3rem; margin-bottom: 10px; }
        p { font-size: 1.5rem; color: #333; margin-bottom: 40px; }

        .btn-container {
            display: flex;
            flex-direction: column;
            gap: 20px;
            width: 80%;
            max-width: 600px;
        }

        .action-btn {
            padding: 40px;
            font-size: 2.5rem;
            font-weight: bold;
            border: 8px solid #ccc;
            border-radius: 20px;
            background: white;
            cursor: pointer;
            transition: all 0.2s;
        }

        /* High Visibility Focus State */
        .action-btn:focus {
            outline: none;
            border-color: #764ba2;
            background-color: #E1BEE7;
            transform: scale(1.05);
        }
    </style>
</head>
<body onload="announceWelcome()">

    <h1>Welcome</h1>
    <p>Use <b>TAB</b> to move and <b>ENTER</b> to select.</p>

    <p><b>Can you</b></p>
    <div class="btn-container">
        <button class="action-btn" onfocus="button_select('See')" onclick="button_click('See')">
            1. See
        </button>
        <button class="action-btn" onfocus="button_select('Hear')" onclick="button_click('Hear')">
            2. Hear
        </button>
        <button class="action-btn" onfocus="button_select('Both')" onclick="button_click('Both')">
            3. Both
        </button>
    </div>

    <script>
        window.addEventListener('keydown', function(event) {
            if (event.key === 'Enter') {
                // Find the element currently focused by Tab
                const focusedElement = document.activeElement;
                
                // If it's one of our buttons, trigger the click
                if (focusedElement && focusedElement.classList.contains('action-btn')) {
                    focusedElement.click();
                }
            }
        });
        function announceWelcome() {
            fetch('/speak?text=Welcome to your AI Assistance. How would you like to interact with me? Can you, See, Hea ,or Both? , Click Tab to switch button, enter to click button', {method: 'POST'});
        }

        function speak(label) {
            fetch(`/speak?text=${label}`, {method: 'POST'});
        }

        function button_click(choice) {
            fetch(`/button_click?text=${choice}`, {method: 'POST'});
            // Add redirection logic here
        }

        function button_select(choice) {
            fetch(`/button_select?text=${choice}`, {method: 'POST'});
            // Add redirection logic here
        }
    </script>
</body>
</html>'''