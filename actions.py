"""
Actions Module
Contains all browser action implementations
Each action is isolated for easy testing and modification
"""

import asyncio
from config import Config


class BrowserActions:
    """Encapsulates all browser action methods"""
    
    def __init__(self, page):
        """
        Initialize with a Playwright page object
        
        Args:
            page: Playwright page instance
        """
        self.page = page
    
    async def navigate(self, url):
        """
        Navigate to a URL
        
        Args:
            url (str): The URL to navigate to
            
        Raises:
            Exception: If navigation fails
        """
        try:
            await self.page.goto(url)
            await self.page.wait_for_load_state("networkidle")
            print(f"✓ Navigated to: {url}")
        except Exception as e:
            raise Exception(f"ERROR [BrowserActions.navigate]: Failed to navigate to '{url}' - {str(e)}")
    
    async def click(self, selector):
        """
        Click an element by selector or visible text
        
        Args:
            selector (str): CSS selector or visible text to click
            
        Raises:
            Exception: If click fails
        """
        try:
            try:
                # Try CSS selector first
                await self.page.click(selector, timeout=Config.CLICK_TIMEOUT)
                print(f"✓ Clicked: {selector}")
            except:
                # Fall back to text matching
                await self.page.get_by_text(selector).first.click(timeout=Config.CLICK_TIMEOUT)
                print(f"✓ Clicked text: {selector}")
        except Exception as e:
            raise Exception(f"ERROR [BrowserActions.click]: Failed to click '{selector}' - {str(e)}")
    
    async def type_text(self, selector, text):
        """
        Type text into an input field
        
        Args:
            selector (str): CSS selector for the input field
            text (str): Text to type
            
        Raises:
            Exception: If typing fails
        """
        try:
            await self.page.fill(selector, text)
            print(f"✓ Typed into {selector}: {text[:50]}{'...' if len(text) > 50 else ''}")
        except Exception as e:
            raise Exception(f"ERROR [BrowserActions.type_text]: Failed to type into '{selector}' - {str(e)}")
    
    async def wait(self, milliseconds):
        """
        Wait for a specified duration
        
        Args:
            milliseconds (int): Time to wait in milliseconds
            
        Raises:
            Exception: If wait fails
        """
        try:
            seconds = int(milliseconds) / 1000
            await asyncio.sleep(seconds)
            print(f"✓ Waited {seconds}s")
        except Exception as e:
            raise Exception(f"ERROR [BrowserActions.wait]: Failed to wait - {str(e)}")
    
    async def scroll(self, direction):
        """
        Scroll the page up or down
        
        Args:
            direction (str): 'up' or 'down'
            
        Raises:
            Exception: If scroll fails
        """
        try:
            pixels = 500 if direction.lower() == "down" else -500
            await self.page.evaluate(f"window.scrollBy(0, {pixels})")
            print(f"✓ Scrolled {direction}")
        except Exception as e:
            raise Exception(f"ERROR [BrowserActions.scroll]: Failed to scroll {direction} - {str(e)}")
    
    async def scroll_to_element(self, selector):
        """
        Scroll to a specific element
        
        Args:
            selector (str): CSS selector for the element
            
        Raises:
            Exception: If scroll fails
        """
        try:
            await self.page.locator(selector).scroll_into_view_if_needed()
            print(f"✓ Scrolled to element: {selector}")
        except Exception as e:
            raise Exception(f"ERROR [BrowserActions.scroll_to_element]: Failed to scroll to '{selector}' - {str(e)}")
    
    async def hover(self, selector):
        """
        Hover over an element
        
        Args:
            selector (str): CSS selector for the element
            
        Raises:
            Exception: If hover fails
        """
        try:
            await self.page.hover(selector)
            print(f"✓ Hovered over: {selector}")
        except Exception as e:
            raise Exception(f"ERROR [BrowserActions.hover]: Failed to hover over '{selector}' - {str(e)}")
    
    async def press_key(self, key):
        """
        Press a keyboard key
        
        Args:
            key (str): Key to press (e.g., 'Enter', 'Escape', 'Tab')
            
        Raises:
            Exception: If key press fails
        """
        try:
            await self.page.keyboard.press(key)
            print(f"✓ Pressed key: {key}")
        except Exception as e:
            raise Exception(f"ERROR [BrowserActions.press_key]: Failed to press key '{key}' - {str(e)}")
    
    async def select_option(self, selector, value):
        """
        Select an option from a dropdown
        
        Args:
            selector (str): CSS selector for the select element
            value (str): Value or text of the option to select
            
        Raises:
            Exception: If selection fails
        """
        try:
            await self.page.select_option(selector, value)
            print(f"✓ Selected option '{value}' in: {selector}")
        except Exception as e:
            raise Exception(f"ERROR [BrowserActions.select_option]: Failed to select '{value}' in '{selector}' - {str(e)}")
    
    async def check_checkbox(self, selector):
        """
        Check a checkbox
        
        Args:
            selector (str): CSS selector for the checkbox
            
        Raises:
            Exception: If check fails
        """
        try:
            await self.page.check(selector)
            print(f"✓ Checked checkbox: {selector}")
        except Exception as e:
            raise Exception(f"ERROR [BrowserActions.check_checkbox]: Failed to check '{selector}' - {str(e)}")
    
    async def uncheck_checkbox(self, selector):
        """
        Uncheck a checkbox
        
        Args:
            selector (str): CSS selector for the checkbox
            
        Raises:
            Exception: If uncheck fails
        """
        try:
            await self.page.uncheck(selector)
            print(f"✓ Unchecked checkbox: {selector}")
        except Exception as e:
            raise Exception(f"ERROR [BrowserActions.uncheck_checkbox]: Failed to uncheck '{selector}' - {str(e)}")
    
    async def screenshot(self, filename):
        """
        Take a screenshot of the page
        
        Args:
            filename (str): Path to save the screenshot
            
        Raises:
            Exception: If screenshot fails
        """
        try:
            await self.page.screenshot(path=filename)
            print(f"✓ Screenshot saved: {filename}")
        except Exception as e:
            raise Exception(f"ERROR [BrowserActions.screenshot]: Failed to take screenshot - {str(e)}")
    
    async def go_back(self):
        """
        Navigate back in browser history
        
        Raises:
            Exception: If navigation fails
        """
        try:
            await self.page.go_back()
            print("✓ Navigated back")
        except Exception as e:
            raise Exception(f"ERROR [BrowserActions.go_back]: Failed to go back - {str(e)}")
    
    async def go_forward(self):
        """
        Navigate forward in browser history
        
        Raises:
            Exception: If navigation fails
        """
        try:
            await self.page.go_forward()
            print("✓ Navigated forward")
        except Exception as e:
            raise Exception(f"ERROR [BrowserActions.go_forward]: Failed to go forward - {str(e)}")
    
    async def reload(self):
        """
        Reload the current page
        
        Raises:
            Exception: If reload fails
        """
        try:
            await self.page.reload()
            print("✓ Page reloaded")
        except Exception as e:
            raise Exception(f"ERROR [BrowserActions.reload]: Failed to reload page - {str(e)}")
    
    async def get_text(self, selector):
        """
        Get text content from an element
        
        Args:
            selector (str): CSS selector for the element
            
        Returns:
            str: Text content of the element
            
        Raises:
            Exception: If getting text fails
        """
        try:
            text = await self.page.locator(selector).text_content()
            print(f"✓ Got text from {selector}: {text[:50]}{'...' if len(text) > 50 else ''}")
            return text
        except Exception as e:
            raise Exception(f"ERROR [BrowserActions.get_text]: Failed to get text from '{selector}' - {str(e)}")
    
    async def get_attribute(self, selector, attribute):
        """
        Get an attribute value from an element
        
        Args:
            selector (str): CSS selector for the element
            attribute (str): Attribute name
            
        Returns:
            str: Attribute value
            
        Raises:
            Exception: If getting attribute fails
        """
        try:
            value = await self.page.locator(selector).get_attribute(attribute)
            print(f"✓ Got {attribute} from {selector}: {value}")
            return value
        except Exception as e:
            raise Exception(f"ERROR [BrowserActions.get_attribute]: Failed to get '{attribute}' from '{selector}' - {str(e)}")
    
    async def execute_javascript(self, script):
        """
        Execute custom JavaScript code
        
        Args:
            script (str): JavaScript code to execute
            
        Returns:
            Any: Result of the JavaScript execution
            
        Raises:
            Exception: If execution fails
        """
        try:
            result = await self.page.evaluate(script)
            print(f"✓ Executed JavaScript")
            return result
        except Exception as e:
            raise Exception(f"ERROR [BrowserActions.execute_javascript]: Failed to execute script - {str(e)}")
    
    async def wait_for_selector(self, selector, timeout=30000):
        """
        Wait for an element to appear
        
        Args:
            selector (str): CSS selector for the element
            timeout (int): Maximum time to wait in milliseconds
            
        Raises:
            Exception: If element doesn't appear
        """
        try:
            await self.page.wait_for_selector(selector, timeout=timeout)
            print(f"✓ Element appeared: {selector}")
        except Exception as e:
            raise Exception(f"ERROR [BrowserActions.wait_for_selector]: Element '{selector}' did not appear - {str(e)}")
    
    async def drag_and_drop(self, source_selector, target_selector):
        """
        Drag an element and drop it onto another
        
        Args:
            source_selector (str): CSS selector for element to drag
            target_selector (str): CSS selector for drop target
            
        Raises:
            Exception: If drag and drop fails
        """
        try:
            await self.page.drag_and_drop(source_selector, target_selector)
            print(f"✓ Dragged {source_selector} to {target_selector}")
        except Exception as e:
            raise Exception(f"ERROR [BrowserActions.drag_and_drop]: Failed to drag '{source_selector}' to '{target_selector}' - {str(e)}")
        
    def get_all_actions(self):
        """Return a list of all available action methods"""
        return [method for method in dir(self) if callable(getattr(self, method)) and not method.startswith("_")]

class ActionExecutor:
    """Executes a list of actions from the AI"""
    
    def __init__(self, browser_actions):
        """
        Initialize with a BrowserActions instance
        
        Args:
            browser_actions (BrowserActions): Instance of BrowserActions
        """
        self.actions = browser_actions
    
    async def execute(self, action_list):
        """
        Execute a list of actions from the AI
        
        Args:
            action_list (list): List of action dictionaries
            
        Returns:
            bool: True if all actions succeeded, False otherwise
        """
        for i, action in enumerate(action_list, 1):
            action_type = action.get("action")
            selector = action.get("selector")
            value = action.get("value")
            description = action.get("description", "")
            
            print(f"\n[{i}/{len(action_list)}] {description}")
            
            try:
                # Route to appropriate action method
                if action_type == "error":
                    print(f"✗ AI reported error: {description}")
                    return False
                
                elif action_type == "navigate":
                    await self.actions.navigate(value)
                
                elif action_type == "click":
                    await self.actions.click(selector)
                
                elif action_type == "type":
                    await self.actions.type_text(selector, value)
                
                elif action_type == "wait":
                    await self.actions.wait(value)
                
                elif action_type == "scroll":
                    await self.actions.scroll(value)
                
                elif action_type == "hover":
                    await self.actions.hover(selector)
                
                elif action_type == "press_key":
                    await self.actions.press_key(value)
                
                elif action_type == "select":
                    await self.actions.select_option(selector, value)
                
                elif action_type == "check":
                    await self.actions.check_checkbox(selector)
                
                elif action_type == "uncheck":
                    await self.actions.uncheck_checkbox(selector)
                
                elif action_type == "back":
                    await self.actions.go_back()
                
                elif action_type == "forward":
                    await self.actions.go_forward()
                
                elif action_type == "reload":
                    await self.actions.reload()
                
                elif action_type == "screenshot":
                    await self.actions.screenshot(value)
                
                else:
                    print(f"✗ Unknown action type: {action_type}")
                    return False
                
                # Small delay between actions for stability
                await asyncio.sleep(0.5)
                
            except Exception as e:
                print(f"✗ {str(e)}")
                return False
        
        print(f"\n✓ All {len(action_list)} actions completed successfully")
        return True