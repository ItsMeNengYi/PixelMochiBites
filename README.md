# AI Browser Control

A browser automation system powered by Google's Gemini AI that provides an overlay interface for controlling any webpage using natural language commands.

## 📁 Project Structure

```
├── app.py                  # Main Flask application (entry point)
├── browser_controller.py   # Coordinates browser and AI operations
├── web_manager.py          # Playwright browser automation
├── ai_agent.py            # Gemini AI integration
├── html_templates.py      # HTML/CSS/JS for overlay and landing page
├── config.py              # Configuration and environment variables
├── requirements.txt       # Python dependencies
├── .env                   # Environment variables (create from .env.example)
└── .env.example          # Template for environment variables
```

## 🚀 Setup

1. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Install Playwright browsers:**
   ```bash
   playwright install chromium
   ```

3. **Set up environment variables:**
   ```bash
   cp .env.example .env
   # Edit .env and add your GEMINI_API_KEY
   ```

4. **Run the application:**
   ```bash
   python app.py
   ```

5. **Open your browser:**
   Navigate to `http://127.0.0.1:5000`

## 🎯 Features

- **Natural Language Control**: Command your browser using plain English
- **AI-Powered**: Gemini AI interprets commands and generates actions
- **Overlay Interface**: Non-intrusive overlay on any webpage
- **Quick Actions**: Pre-built buttons for common tasks
- **Page Simplification**: Remove clutter and focus on content

## 📝 Usage

### Starting the Browser
1. Open `http://127.0.0.1:5000` in your browser
2. Click "Start Browser"
3. A new browser window opens with the AI control overlay

### Executing Commands
Type natural language commands like:
- "Search for Python tutorials"
- "Click the login button"
- "Scroll down"
- "Navigate to github.com"

### Quick Actions
- **Scroll Down/Up**: Navigate the page
- **Go Back**: Return to previous page
- **Simplify**: Remove ads and clutter

## 🔧 Configuration

Edit `config.py` to customize:
- Flask host and port
- Browser settings (headless mode, flags)
- Timeouts for operations
- API keys

## 🛡️ Error Handling

All errors are logged with clear prefixes showing their origin:
- `ERROR [Config]`: Configuration issues
- `ERROR [AIAgent]`: AI/Gemini errors
- `ERROR [WebManager]`: Browser automation errors
- `ERROR [BrowserController]`: Coordination errors
- `ERROR [app]`: Flask application errors

## 📦 Module Descriptions

### `app.py`
- Flask web server
- HTTP routes (`/start`, `/execute`, `/simplify`, `/restore`)
- Request handling and error responses

### `browser_controller.py`
- High-level controller
- Coordinates WebManager and AIAgent
- Manages command execution flow

### `web_manager.py`
- Playwright browser automation
- Page interaction (click, type, scroll, navigate)
- Overlay injection
- Page simplification

### `ai_agent.py`
- Gemini AI integration
- Command interpretation
- Action generation from natural language

### `html_templates.py`
- Landing page HTML
- Overlay HTML/CSS/JavaScript
- All frontend code in one place

### `config.py`
- Environment variables
- Application settings
- Configuration validation

## 🔍 Troubleshooting

**Browser won't start:**
- Check if Playwright is installed: `playwright install chromium`
- Verify GEMINI_API_KEY is set in .env

**Commands not working:**
- Check console output for error messages
- All errors show which module they originated from
- Ensure the browser window is visible (not minimized)

**Overlay not appearing:**
- Check browser console for JavaScript errors
- Ensure CORS is enabled in browser

## 📄 License

MIT License - feel free to modify and use as needed!