"""
Configuration Module
Handles environment variables and application settings
"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    """Application configuration"""
    
    # API Keys
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    
    # Flask settings
    FLASK_HOST = '127.0.0.1'
    FLASK_PORT = 5000
    FLASK_DEBUG = False
    
    # Browser settings
    BROWSER_HEADLESS = False
    BROWSER_ARGS = [
        "--disable-web-security",
        "--allow-running-insecure-content"
    ]
    
    # Timeouts (in seconds)
    COMMAND_TIMEOUT = 30
    SIMPLIFY_TIMEOUT = 10
    RESTORE_TIMEOUT = 10
    CLICK_TIMEOUT = 5000  # milliseconds

    INTERACTION_MODE = 'both' # Default
    INPUT_MODE = 'keyboard'   # Default
    PAGE = "/"

    @classmethod
    def set_setting(cls, key, value):
        """
        Dynamically set a configuration value.
        Usage: Config.set_setting('INTERACTION_MODE', 'see')
        """
        # Convert key to uppercase to match class attribute naming convention
        key = key.upper()
        
        if hasattr(cls, key):
            setattr(cls, key, value)
            print(f"⚙️ [Config]: {key} updated to -> {value}")
        else:
            print(f"⚠️ [Config]: Setting '{key}' does not exist.")
    
    @classmethod
    def validate(cls):
        """Validate required configuration"""
        if not cls.GEMINI_API_KEY:
            raise ValueError("ERROR [Config]: GEMINI_API_KEY not found in environment variables")
        return True
    
    def next_page():
        if Config.PAGE == "/":
            Config.PAGE = "/input_selection"
            return "/input_selection"
        if Config.PAGE == "/input_selection":
            Config.PAGE = "/browser"
            return "/browser"
        if Config.PAGE == "/browser":
            return None
        
    def previous_page():
        if Config.PAGE == "/browser":
            Config.PAGE = "/input_selection"
            return "/input_selection"
        if Config.PAGE == "/input_selection":
            Config.PAGE = "/"
            return "/"
        if Config.PAGE == "/":
            return None
    
# Export config instance