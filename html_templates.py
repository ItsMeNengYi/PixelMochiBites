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
        <button class="action-btn" onfocus="button_select('see')" onclick="button_click('see')">
            1. See
        </button>
        <button class="action-btn" onfocus="button_select('hear')" onclick="button_click('hear')">
            2. Hear
        </button>
        <button class="action-btn" onfocus="button_select('both')" onclick="button_click('both')">
            3. Both
        </button>
    </div>

    <script>
        function announceWelcome() {
            fetch('/speak?text=Welcome to your AI Assistance. How would you like to interact with me? Can you, See, Hear, or Both? Click Tab to switch button, enter to click button', {method: 'POST'});
        }

        function speak(label) {
            fetch(`/speak?text=${label}`, {method: 'POST'});
        }
        
        function button_click(choice) {
            fetch(`/button_click?text=${choice}`, {method: 'POST'});
        }

        function button_select(choice) {
            fetch(`/button_select?text=${choice}`, {method: 'POST'});
        }

        setInterval(() => {
            fetch('/get_current_state')
                .then(response => response.json())
                .then(data => {
                    const pythonPage = data.current_page;
                    const browserPage = window.location.pathname;

                    // If Python changed the state, move the browser automatically
                    if (pythonPage !== browserPage) {
                        window.location.href = pythonPage;
                    }
                });
        }, 500);
    </script>
</body>
</html>'''

def get_select_interact_page_html():
    """Returns the HTML for the Input Type selection page"""
    return '''<!DOCTYPE html>
<html>
<head>
    <style>
        body {
            font-family: sans-serif;
            background-color: #FFFDE7;
            display: flex;
            flex-direction: column;
            align-items: center;
            padding: 50px;
            min-height: 100vh;
        }
        h1 { font-size: 3rem; margin-bottom: 40px; text-transform: uppercase; text-align: center; }
        
        .btn-container {
            display: flex;
            flex-direction: column;
            gap: 25px;
            width: 80%;
            max-width: 600px;
        }

        .action-btn {
            padding: 50px;
            font-size: 2.5rem;
            font-weight: bold;
            border: 8px solid #444;
            border-radius: 25px;
            background: #90CAF9; /* Matches the blue in your screenshot */
            cursor: pointer;
            transition: all 0.2s;
        }

        .back-btn {
            margin-top: 50px;
            padding: 20px 40px;
            font-size: 1.5rem;
            background-color: #C6FF00; /* Matches the green 'back' button */
            border: 4px solid #444;
            border-radius: 15px;
            font-weight: bold;
            cursor: pointer;
        }

        /* High Visibility Focus State */
        .action-btn:focus, .back-btn:focus {
            outline: 10px solid #764ba2;
            background-color: #E1BEE7;
            transform: scale(1.05);
        }
    </style>
</head>
<body onload="announcePage()">

    <h1>Select Your Input Type</h1>

    <div class="btn-container">
        <button class="action-btn" 
                onfocus="button_select('Keyboard')" 
                onclick="button_click('keyboard')">
            keyboard
        </button>
        
        <button class="action-btn" 
                onfocus="button_select('Speech')" 
                onclick="button_click('speech')">
            speech
        </button>
    </div>

    <button class="back-btn" onfocus="button_select('Back')" onclick="button_click('back')">
        back
    </button>

    <script>
        // Automatic Focus on load for immediate 'Enter' support
        function announcePage() {
            fetch('/speak?text=Select your input type. Keyboard or Speech?', {method: 'POST'});
        }

        function speak(label) {
            fetch(`/speak?text=${label}`, {method: 'POST'});
        }
        
        function button_click(choice) {
            fetch(`/button_click?text=${choice}`, {method: 'POST'});
        }

        function button_select(choice) {
            fetch(`/button_select?text=${choice}`, {method: 'POST'});
        }

        setInterval(() => {
            fetch('/get_current_state')
                .then(response => response.json())
                .then(data => {
                    const pythonPage = data.current_page;
                    const browserPage = window.location.pathname;

                    // If Python changed the state, move the browser automatically
                    if (pythonPage !== browserPage) {
                        window.location.href = pythonPage;
                    }
                });
        }, 500);
    </script>
</body>
</html>'''


def get_browser_page_html():
    """Returns the HTML for the URL browsing interface"""
    return '''<!DOCTYPE html>
<html>
<head>
    <style>
        body {
            font-family: sans-serif;
            background-color: #FFFDE7;
            display: flex;
            flex-direction: column;
            align-items: center;
            padding: 40px;
            min-height: 100vh;
            margin: 0;
        }

        h1 { font-size: 2.5rem; color: #333; margin-bottom: 20px; }

        .browser-container {
            width: 90%;
            max-width: 800px;
            display: flex;
            flex-direction: column;
            gap: 30px;
        }

        /* Large, accessible input field */
        .url-input {
            padding: 30px;
            font-size: 2rem;
            border: 6px solid #444;
            border-radius: 20px;
            width: 100%;
            box-sizing: border-box;
        }

        .url-input:focus {
            outline: 6px solid #764ba2;
            background-color: #F3E5F5;
        }

        .go-btn {
            padding: 40px;
            font-size: 3rem;
            font-weight: bold;
            background-color: #C6FF00; /* High visibility green */
            border: 6px solid #444;
            border-radius: 25px;
            cursor: pointer;
            transition: transform 0.1s;
        }

        .go-btn:focus {
            outline: 8px solid #764ba2;
            background-color: #E1BEE7;
            transform: scale(1.02);
        }

        .status-msg {
            font-size: 1.5rem;
            color: #666;
            margin-top: 20px;
        }
    </style>
</head>
<body onload="announceBrowser()">

    <h1>What would you like to do?</h1>
    
    <div class="browser-container">
        <input type="text" id="urlInput" class="url-input" 
               placeholder="Type website address or intention here..."
               onfocus="button_select('input area')" />
        
        <button class="go-btn" id="goBtn"
                onfocus="button_select('Go button')" 
                onclick="button_click(document.getElementById('urlInput').value)">
            GO
        </button>
    </div>

    <p class="status-msg">Press <b>TAB</b> to switch, <b>ENTER</b> to select.</p>

    <script>
        function announceBrowser() {
            fetch('/speak?text=Please say your intention loud.', {method: 'POST'});
        }
        
        function button_click(choice) {
            fetch(`/button_click?text=${choice}`, {method: 'POST'});
        }

        function button_select(choice) {
            fetch(`/button_select?text=${choice}`, {method: 'POST'});
        }

    </script>
</body>
</html>'''