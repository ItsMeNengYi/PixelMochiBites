"""
Web Manager Module
Handles browser automation using Playwright
"""

import asyncio
from playwright.async_api import async_playwright
from config import Config
from html_templates import get_overlay_script
from actions import BrowserActions, ActionExecutor

class WebManager:
    """Manages browser instance and page interactions"""
    
    def __init__(self):
        """Initialize the web manager"""
        self.page = None
        self.browser = None
        self.context = None
        self.loop = None
        self.original_html = {}
        self.playwright_instance = None
        self.action_executor = None  # Will be initialized after browser starts
        print("✓ WebManager initialized")
    
    async def start_browser(self):
        """
        Start the browser with security settings
        
        Raises:
            Exception: If browser fails to start
        """
        try:
            print("→ Starting browser...")
            
            # Start Playwright
            self.playwright_instance = await async_playwright().start()
            
            # Launch browser with custom flags
            self.browser = await self.playwright_instance.chromium.launch(
                headless=Config.BROWSER_HEADLESS,
                args=Config.BROWSER_ARGS
            )
            
            # Create context with HTTPS error handling
            self.context = await self.browser.new_context(ignore_https_errors=True)
            self.page = await self.context.new_page()
            
            # Set up page load event listener
            self.page.on("load", lambda: asyncio.create_task(self._on_page_load()))
            
            # Initialize action executor with the page
            browser_actions = BrowserActions(self.page)
            self.action_executor = ActionExecutor(browser_actions)
            
            print("✓ Browser started successfully")
            
        except Exception as e:
            raise Exception(f"ERROR [WebManager.start_browser]: Failed to start browser - {str(e)}")
    
    async def _on_page_load(self):
        """Called automatically when page loads"""
        try:
            await asyncio.sleep(0.3)
            await self._inject_overlay()
        except Exception as e:
            print(f"ERROR [WebManager._on_page_load]: Failed to inject overlay - {str(e)}")
    
    async def _inject_overlay(self):
        """Inject the AI control overlay into the current page"""
        try:
            overlay_script = get_overlay_script()
            await self.page.evaluate(overlay_script)
            print("✓ Overlay injected")
        except Exception as e:
            raise Exception(f"ERROR [WebManager._inject_overlay]: Failed to inject overlay - {str(e)}")
    
    async def get_page_context(self):
        """
        Get current page information for AI
        
        Returns:
            dict: Page context with url, title, and html
            
        Raises:
            Exception: If page access fails
        """
        try:
            url = self.page.url
            title = await self.page.title()
            html = await self.page.content()
            
            return {
                "url": url,
                "title": title,
                "html": html
            }
        except Exception as e:
            raise Exception(f"ERROR [WebManager.get_page_context]: Failed to get page context - {str(e)}")
    
    async def execute_actions(self, actions):
        """
        Execute a list of actions on the page
        
        Args:
            actions (list): List of action dictionaries from AI
            
        Returns:
            bool: True if all actions succeeded, False otherwise
        """
        try:
            return await self.action_executor.execute(actions)
        except Exception as e:
            print(f"ERROR [WebManager.execute_actions]: {str(e)}")
            return False
    
    async def simplify_page(self):
        """
        Simplify the current page by removing unnecessary elements
        
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            url = self.page.url
            
            # Store original HTML
            if url not in self.original_html:
                self.original_html[url] = await self.page.content()
            
            # Simplification script
            simplify_script = """
            (function() {
                // Remove common clutter
                const selectorsToRemove = [
                    'script', 'style', 'iframe', 'noscript',
                    '[role="banner"]', '[role="navigation"]',
                    'header', 'footer', 'nav', 'aside',
                    '.advertisement', '.ads', '.cookie-banner',
                    '.popup', '.modal', '.sidebar'
                ];
                
                selectorsToRemove.forEach(selector => {
                    document.querySelectorAll(selector).forEach(el => el.remove());
                });
                
                // Keep only main content
                const main = document.querySelector('main, article, [role="main"], .content, #content');
                if (main) {
                    document.body.innerHTML = main.outerHTML;
                }
                
                // Apply clean styling
                document.body.style.cssText = `
                    max-width: 800px; margin: 0 auto; padding: 20px;
                    font-family: Georgia, serif; font-size: 18px;
                    line-height: 1.6; background: white; color: #333;
                `;
            })();
            """
            
            await self.page.evaluate(simplify_script)
            print("✓ Page simplified")
            return True
            
        except Exception as e:
            print(f"ERROR [WebManager.simplify_page]: Simplification failed - {str(e)}")
            return False
    
    async def restore_original_html(self):
        """
        Restore the page to its original state
        
        Returns:
            bool: True if successful, False if no original found
        """
        try:
            url = self.page.url
            
            if url not in self.original_html:
                print("✗ No original HTML to restore")
                return False
            
            await self.page.set_content(self.original_html[url])
            print("✓ Page restored to original state")
            return True
            
        except Exception as e:
            print(f"ERROR [WebManager.restore_original_html]: Restore failed - {str(e)}")
            return False
    
    async def close(self):
        """Close the browser and cleanup"""
        try:
            if self.browser:
                await self.browser.close()
            if self.playwright_instance:
                await self.playwright_instance.stop()
            print("✓ Browser closed")
        except Exception as e:
            print(f"ERROR [WebManager.close]: Cleanup failed - {str(e)}")