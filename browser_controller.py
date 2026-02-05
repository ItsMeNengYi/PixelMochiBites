"""
Browser Controller Module
Coordinates between WebManager and AIAgent
"""

from web_manager import WebManager
from ai_agent import AIAgent

class BrowserController:
    """High-level controller that coordinates browser and AI operations"""
    
    def __init__(self, web_manager=None, ai_agent=None):
        """Initialize controller with web manager and AI agent"""
        try:
            self.web_manager = web_manager if web_manager else WebManager()
            self.ai_agent = ai_agent if ai_agent else AIAgent()
            print("✓ BrowserController initialized")
        except Exception as e:
            raise Exception(f"ERROR [BrowserController.__init__]: Initialization failed - {str(e)}")
    
    async def start_browser(self):
        """
        Start the browser
        
        Raises:
            Exception: If browser startup fails
        """
        try:
            await self.web_manager.start_browser()
        except Exception as e:
            raise Exception(f"ERROR [BrowserController.start_browser]: {str(e)}")
    
    async def execute_command(self, command):
        """
        Execute a natural language command
        
        Args:
            command (str): User's command in natural language
            
        Returns:
            bool: True if command executed successfully, False otherwise
        """
        try:
            # Get current page context
            context = await self.web_manager.get_page_context()
            
            # Ask AI to interpret the command
            actions = await self.ai_agent.interpret_command(command, context)
            
            # Execute the actions
            success = await self.web_manager.execute_actions(actions)
            
            return success
            
        except Exception as e:
            print(f"ERROR [BrowserController.execute_command]: {str(e)}")
            return False
    
    async def simplify_page(self):
        """
        Simplify the current page
        
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            return await self.web_manager.simplify_page()
        except Exception as e:
            print(f"ERROR [BrowserController.simplify_page]: {str(e)}")
            return False
    
    async def restore_page(self):
        """
        Restore the page to original state
        
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            return await self.web_manager.restore_original_html()
        except Exception as e:
            print(f"ERROR [BrowserController.restore_page]: {str(e)}")
            return False
    
    async def navigate_to(self, url):
        """
        Navigate to a specific URL
        
        Args:
            url (str): URL to navigate to
        """
        try:
            await self.web_manager.page.goto(url)
            await self.web_manager.page.wait_for_load_state("networkidle")
        except Exception as e:
            raise Exception(f"ERROR [BrowserController.navigate_to]: Navigation to '{url}' failed - {str(e)}")
    
    async def close(self):
        """Close the browser"""
        try:
            await self.web_manager.close()
        except Exception as e:
            print(f"ERROR [BrowserController.close]: {str(e)}")