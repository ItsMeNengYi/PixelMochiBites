"""
AI Agent Module
Handles all interactions with Google's Gemini API
"""

import json
import google.generativeai as genai
from config import Config

class AIAgent:
    """Handles AI-powered command interpretation and action generation"""
    
    def __init__(self):
        """Initialize the AI agent with Gemini"""
        try:
            genai.configure(api_key=Config.GEMINI_API_KEY)
            self.model = genai.GenerativeModel("gemini-2.5-flash-lite")
            print("✓ AI Agent initialized successfully")
        except Exception as e:
            raise Exception(f"ERROR [AIAgent.__init__]: Failed to initialize Gemini - {str(e)}")
        
    async def navigate_url(self, user_command):
        """
        Interprets user command to find a target URL.
        Returns: {'url': str or None, 'description': str}
        """
        prompt = f"""
        You are a navigation assistant for a simplified web browser.
        Analyze the user's command and extract a target URL.
        
        Rules:
        1. If the user mentions a specific website (e.g., "Google", "YouTube", "NUS"), 
           provide the full HTTPS URL.
        2. If the user command is vague or doesn't specify a destination, 
           return null for the url.
        3. Provide a brief, friendly description of what you are doing.

        User Command: "{user_command}"

        Return ONLY a JSON object in this format:
        {{"url": "https://example.com", "description": "Navigating to example"}}
        """
        try:
            # Using generation_config to enforce JSON mode
            response = self.model.generate_content(
                prompt,
                generation_config={"response_mime_type": "application/json"}
            )
            
            # Parse the JSON string from Gemini into a Python dictionary
            result = json.loads(response.text)
            
            # Safety check: Ensure the keys exist
            return {
                "url": result.get("url"),
                "description": result.get("description", "Processing your request.")
            }

        except Exception as e:
            print(f"⚠️ [AIAgent]: Error interpreting command: {e}")
            return {"url": None, "description": "I'm sorry, I couldn't understand that command."}
    
    async def interpret_command(self, command, page_context):
        """
        Send command to Gemini and get back structured actions
        
        Args:
            command (str): User's natural language command
            page_context (dict): Current page information (url, title, html)
            
        Returns:
            list: List of action dictionaries
            
        Raises:
            Exception: If Gemini API call fails
        """
        try:
            prompt = self._build_prompt(command, page_context)
            
            print(f"→ Sending to Gemini: {command}")
            response = self.model.generate_content(prompt)
            
            # Parse JSON response
            actions = self._parse_response(response.text)
            print(f"✓ Received {len(actions)} actions from AI")
            
            return actions
            
        except json.JSONDecodeError as e:
            raise Exception(f"ERROR [AIAgent.interpret_command]: Failed to parse AI response as JSON - {str(e)}")
        except Exception as e:
            raise Exception(f"ERROR [AIAgent.interpret_command]: Gemini API call failed - {str(e)}")
    
    def _build_prompt(self, command, context):
        """Build the prompt for Gemini"""
        return f"""You are a browser automation assistant. Given a user command and page context, return a JSON array of actions.

Current Page:
URL: {context['url']}
Title: {context['title']}

Page HTML (simplified):
{context['html'][:3000]}

User Command: "{command}"

Return ONLY a JSON array with this structure:
[
  {{"action": "navigate", "value": "https://example.com", "description": "Navigate to URL"}},
  {{"action": "click", "selector": "button.submit", "description": "Click submit button"}},
  {{"action": "type", "selector": "input[name='search']", "value": "search text", "description": "Type in search box"}},
  {{"action": "scroll", "value": "down", "description": "Scroll down"}},
  {{"action": "wait", "value": "2000", "description": "Wait 2 seconds"}},
  {{"action": "error", "description": "Cannot complete - explain why"}}
]

Rules:
- Use CSS selectors or visible text for elements
- For clicks without clear selector, use visible button/link text
- Scroll value can be "up" or "down"
- Wait value in milliseconds
- Return error action if command is unclear or impossible
- ONLY return valid JSON, no markdown, no explanation"""
    
    def _parse_response(self, response_text):
        """Parse and validate Gemini's response"""
        try:
            # Remove markdown code blocks if present
            clean_text = response_text.strip()
            if clean_text.startswith("```json"):
                clean_text = clean_text[7:]
            if clean_text.startswith("```"):
                clean_text = clean_text[3:]
            if clean_text.endswith("```"):
                clean_text = clean_text[:-3]
            
            clean_text = clean_text.strip()
            
            # Parse JSON
            actions = json.loads(clean_text)
            
            if not isinstance(actions, list):
                raise ValueError("Response is not a JSON array")
            
            return actions
            
        except Exception as e:
            raise Exception(f"ERROR [AIAgent._parse_response]: Invalid response format - {str(e)}")
        