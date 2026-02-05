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
    
    @classmethod
    def validate(cls):
        """Validate required configuration"""
        if not cls.GEMINI_API_KEY:
            raise ValueError("ERROR [Config]: GEMINI_API_KEY not found in environment variables")
        return True