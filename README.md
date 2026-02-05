# Playwright + Gemini Browser Automation

Control your browser with natural language using Playwright and Google's Gemini API.

## Features

- 🎯 Natural language browser control
- ⌨️ Text input support
- 🤖 AI-powered action interpretation via Gemini
- 🔄 Multi-step automation sequences
- 📋 Automatic page context extraction
- 🖥️ Both CLI and GUI interfaces

## Prerequisites

- Python 3.8+
- Google Gemini API key ([Get one here](https://makersuite.google.com/app/apikey))

## Installation

### 1. Clone or download the project files

### 2. Install Python dependencies

```bash
pip install -r requirements.txt
```

### 3. Install Playwright browsers
```bash
playwright install chromium
```

### 4. Set up your Gemini API key

Create a `.env` file:
```bash
cp .env.example .env
```

Edit `.env` and add your API key:
```
GEMINI_API_KEY=your-actual-api-key-here
```

Or set it as an environment variable:
```bash
export GEMINI_API_KEY=your-actual-api-key-here
```

## Usage

### Web Interface with Overlay (Recommended - Best Experience!)

```bash
python playwright_gemini_web.py
```

Then open http://localhost:5000 in your browser to start.

**Features:**
- 🎨 Beautiful floating overlay on any webpage
- ⌨️ Text input field for commands
- 🎯 Quick action buttons (scroll, back, simplify)
- ✨ **Simplify page** for cognitive accessibility
- 🔄 **Restore original** HTML anytime
- 📱 Works on top of any website

### Command Line Version

```bash
python playwright_gemini_automation.py
```

Interactive terminal-based control - type commands directly.

### GUI Version (Separate Window)

```bash
python playwright_gemini_gui.py
```

Opens a separate window with browser controls.

## Example Commands

Once running, try these commands:

- `"search for cats"` - Types in search box and submits
- `"click the first search result"` - Clicks first result
- `"go to youtube.com"` - Navigates to YouTube
- `"scroll down"` - Scrolls the page down
- `"type hello world in the search box"` - Enters text
- `"click the login button"` - Finds and clicks login

## Accessibility Features (Web Version)

The web interface includes a **Simplify** button that transforms any webpage for cognitive accessibility:

**What it does:**
- ✨ Removes distracting elements (ads, popups, sidebars)
- 📝 Increases font size to 18px
- 📐 Improves line spacing and readability
- 🎨 Simplifies colors to high contrast
- 🔲 Removes animations and complex layouts
- 💾 **Saves original HTML** before simplification
- 🔄 One-click restore to original

**Perfect for users with:**
- Cognitive impairments
- Reading difficulties
- Attention challenges
- Visual processing issues

Click "Simplify" in the overlay or say `"simplify this page"` to activate!

## How It Works

1. **Command Input**: You provide a natural language command (voice or text)
2. **Context Extraction**: The system extracts current page info (URL, buttons, inputs)
3. **AI Interpretation**: Gemini converts your command into structured actions
4. **Execution**: Playwright executes the actions on the browser

## Action Format

Gemini returns actions in this JSON format:

```json
[
    {
        "action": "click",
        "selector": "button.login",
        "description": "Click login button"
    },
    {
        "action": "type",
        "selector": "input[name='email']",
        "value": "user@example.com",
        "description": "Enter email"
    }
]
```

Supported actions:
- `click` - Click an element
- `type` - Type text into input
- `navigate` - Go to URL
- `wait` - Wait for milliseconds
- `scroll` - Scroll up/down

## Customization

### Modify the Gemini Prompt

Edit the `send_to_gemini()` method to customize how commands are interpreted.

### Add New Actions

Extend the `execute_actions()` method to support additional action types.

### Change Browser Settings

Modify `start_browser()` to change headless mode, viewport size, etc:

```python
await controller.start_browser(headless=True)  # Run without visible browser
```

## Troubleshooting

**"ModuleNotFoundError: No module named 'playwright'"**
```bash
pip install playwright
playwright install chromium
```

**Gemini API errors:**
- Verify your API key is correct in `.env` file
- Check your API quota at [Google AI Studio](https://makersuite.google.com)
- Make sure you have the `GEMINI_API_KEY` environment variable set

**Playwright errors:**
- Run `playwright install chromium` to download browsers
- Check browser compatibility
- Try running with `headless=True` in the code

**Element not found:**
- The AI may need better page context
- Try being more specific in your command
- Inspect the page to verify elements exist
- Check the activity log to see what selectors were tried

## Security Notes

- Never commit your `.env` file with real API keys
- Be careful when automating actions on sensitive sites
- This tool has full browser control - use responsibly

## License

MIT License - feel free to modify and use as needed.

## Contributing

Suggestions and improvements welcome! This is a base implementation designed to be extended.