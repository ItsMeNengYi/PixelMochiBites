# Web Overlay Interface Guide

The web interface provides a browser extension-like overlay that sits on top of any webpage you visit.

## Quick Start

```bash
# Start the web server
python playwright_gemini_web.py

# Open http://localhost:5000 in your browser
# Click "Start Browser"
```

## Interface Overview

### Floating Control Panel

The control panel appears in the top-right corner of every page you visit:

```
┌─────────────────────────────┐
│ 🤖 AI Browser Control [Hide]│
├─────────────────────────────┤
│ [Type your command...]      │
│ [Execute]                   │
│                             │
│ [⬇️ Scroll] [⬆️ Scroll]     │
│ [⬅️ Back]   [✨ Simplify]   │
│                             │
│ Status: Ready               │
└─────────────────────────────┘
```

## Features

### 1. Command Input
Type natural language commands:
- "search for cats"
- "click the login button"
- "fill in email with test@example.com"
- "go to youtube.com"

### 2. Quick Action Buttons
- **⬇️ Scroll Down** - Scroll page down
- **⬆️ Scroll Up** - Scroll page up
- **⬅️ Go Back** - Browser back button
- **✨ Simplify** - Transform page for accessibility

### 3. Simplify Page Feature

The **Simplify** button transforms any webpage for users with cognitive impairments:

**Before Simplification:**
- Cluttered layout with ads
- Small, hard-to-read text
- Distracting animations
- Complex navigation
- Multiple sidebars and popups

**After Simplification:**
- Clean, centered content
- Large 18px font
- High contrast colors
- No animations
- Only essential content
- Wider line spacing

**What Gets Removed:**
- Advertisements
- Sidebars
- Popups and modals
- Social sharing buttons
- Comments sections
- Navigation bars (except main)
- Footer links
- Related posts
- Cookie banners

**What Gets Enhanced:**
- Font size increased to 18px
- Line height increased to 1.8
- Headers made bold and clear
- Links made more visible
- Buttons made larger
- Content centered with max-width
- High contrast black text on white

### 4. Original HTML Preservation

**Automatic Backup:**
When you click "Simplify", the system automatically saves the original HTML of the page.

**Restore Anytime:**
A "🔄 Restore Original" button appears at the bottom-right when a page is simplified.

**Storage:**
Original HTML is stored in memory per URL, so you can navigate away and come back.

## How It Works

### Architecture

```
┌─────────────────┐
│   Your Browser  │ ← You interact with this
└────────┬────────┘
         │
         ↓
┌─────────────────┐
│  Flask Server   │ ← Runs on localhost:5000
│  (Port 5000)    │
└────────┬────────┘
         │
         ↓
┌─────────────────┐
│   Playwright    │ ← Controls the browser
│     Browser     │
└────────┬────────┘
         │
         ↓
┌─────────────────┐
│  Gemini API     │ ← Interprets commands
└─────────────────┘
```

### Flow

1. **User types command** in overlay input
2. **JavaScript sends** command to Flask server (http://localhost:5000/execute)
3. **Flask server** gets page context from Playwright
4. **Gemini API** converts command to actions
5. **Playwright** executes actions on the page
6. **User sees** the result immediately

## Advanced Usage

### Customizing the Overlay

Edit the `_inject_overlay()` function in `playwright_gemini_web.py`:

```python
# Change position
top: 10px;    # Change to bottom: 10px;
right: 10px;  # Change to left: 10px;

# Change colors
background: linear-gradient(...);  # Your gradient

# Change size
width: 350px;  # Make wider/narrower
```

### Adding Custom Quick Buttons

In the overlay HTML, add more buttons:

```javascript
<button onclick="executeQuick('your command')" class="quick-btn">
    🎯 Your Label
</button>
```

### Customizing Simplification

Edit the `simplify_page()` function:

```python
# Change font size
font-size: 18px !important;  # Make larger/smaller

# Change max width
max-width: 900px !important;  # Wider or narrower

# Add/remove elements to hide
selectorsToRemove = [
    'your-selector-here',
    '.your-class',
    '#your-id'
]
```

## Accessibility Best Practices

### For Cognitive Impairments

The simplified view follows WCAG AAA guidelines:

1. **Large Text**: 18px minimum (AAA requires 14pt/18.5px)
2. **Line Height**: 1.8 (AAA recommends 1.5 minimum)
3. **Contrast**: Black on white (AAA ratio: 7:1)
4. **Spacing**: Generous margins and padding
5. **No Distractions**: Animations and auto-play removed
6. **Clear Hierarchy**: Bold headers, clear structure
7. **Simple Language**: Original content preserved
8. **Focus**: Only essential content visible

### Customizing for Specific Needs

**Dyslexia:**
```css
font-family: 'OpenDyslexic', Arial, sans-serif;
letter-spacing: 0.12em;
word-spacing: 0.16em;
```

**Low Vision:**
```css
font-size: 24px;
line-height: 2;
font-weight: 600;
```

**ADHD:**
```css
/* Already removes distractions */
/* Add focus mode: */
filter: grayscale(50%);  /* Reduce color stimulation */
```

## Tips & Tricks

### Hide the Overlay
Click the "Hide" button in the overlay header. Refresh the page to show it again.

### Pin to Specific Sites
Modify the overlay injection to only show on certain domains:

```javascript
if (window.location.hostname === 'example.com') {
    // Inject overlay
}
```

### Export Simplified HTML
Add a button to download the simplified version:

```javascript
const html = document.documentElement.outerHTML;
const blob = new Blob([html], {type: 'text/html'});
const url = URL.createObjectURL(blob);
```

## Troubleshooting

**Overlay doesn't appear:**
- Check if JavaScript is enabled
- Look for browser console errors
- Try refreshing the page

**Simplify doesn't work:**
- Some pages use shadow DOM (won't simplify)
- Check if page loaded completely
- Try navigating to the page again

**Commands fail:**
- Check Flask server is running (localhost:5000)
- Check Gemini API key is set
- Look at server console for errors

**Original restore doesn't work:**
- Original is only saved when you click Simplify
- Navigating away clears the saved original
- Try simplifying again to re-save

## Security Note

The overlay communicates with localhost:5000. It only works on your local machine and cannot be accessed remotely unless you configure Flask to accept external connections.

The system does NOT:
- Send data to external servers (except Gemini API)
- Store your browsing history
- Track your activity
- Inject malicious code

All automation happens locally on your machine.