# from autogen import Agent

# class DebuggingAgent(Agent):
#     def __init__(self):
#         super().__init__("DebuggingAgent")

#     def run(self, code: str) -> str:
#         # Placeholder for debugging logic
#         return f"Debugged code: {code}"

import logging
from typing import Dict, Any, List, Optional
import autogen
from openai import OpenAI

from backend.services.rag import RAGService

# Configure logging
logger = logging.getLogger(__name__)

class DebuggingAgent:
    """Agent for debugging code."""
    
    def __init__(self, openai_api_key: str, openai_model: str, rag_service: RAGService):
        """
        Initialize the Debugging Agent.
        
        Args:
            openai_api_key: API key for OpenAI
            openai_model: OpenAI model to use
            rag_service: RAG service for retrieving relevant context
        """
        self.openai_api_key = openai_api_key
        self.openai_model = openai_model
        self.rag_service = rag_service
        self.client = OpenAI(api_key=openai_api_key)
        
        # Configure the AutoGen agent
        self.agent = self._setup_agent()
        
        logger.info("Debugging Agent initialized")
    
    def _setup_agent(self):
        """Set up the AutoGen agent for debugging."""
        config_list = [
            {
                "model": self.openai_model,
                "api_key": self.openai_api_key,
            }
        ]
        
        # Create the AutoGen agent
        debugging_agent = autogen.AssistantAgent(
            name="debugging_agent",
            llm_config={"config_list": config_list},
            system_message="""
            You are an expert code debugger. You analyze code to:
            1. Identify bugs and logical errors
            2. Fix security vulnerabilities
            3. Check for edge cases that might cause failures
            4. Ensure proper error handling
            5. Verify that the code meets the intended functionality
            
            When you find issues, you fix them directly in the code.
            """
        )
        
        return debugging_agent
    
    def debug_code(self, code: str, language: str, error_messages: Optional[List[str]] = None) -> str:
        """
        Debug the provided code.
        
        Args:
            code: Code to debug
            language: Programming language of the code
            error_messages: Optional list of error messages
            
        Returns:
            Debugged code
        """
        logger.info(f"Debugging {language} code: {code[:50]}...")
        
        # Use RAG to retrieve relevant debugging patterns
        context = self.rag_service.retrieve(f"debugging {language} code common errors")
        
        # Format code and context for the LLM
        messages = [
            {
                "role": "system", 
                "content": f"""
                You are an expert {language} code debugger. Your task is to analyze the code,
                identify any issues, and provide a corrected version.
                """
            },
            {
                "role": "user", 
                "content": f"""
                I need you to debug the following {language} code:
                
                ```{language}
                {code}
                ```
                
                {f'ERROR MESSAGES:\n' + '\n'.join(error_messages) if error_messages else ''}
                
                {f'RELEVANT DEBUGGING PATTERNS: {context}' if context else ''}
                
                Please identify and fix any bugs, logical errors, security vulnerabilities, 
                edge cases, and improve error handling. Return the complete corrected code
                without explanations outside of code comments. Add comments for significant changes.
                """
            }
        ]
        
        # Call the OpenAI API
        response = self.client.chat.completions.create(
            model=self.openai_model,
            messages=messages,
            temperature=0.1,
            max_tokens=4000
        )
        
        debugged_code = response.choices[0].message.content
        
        # Extract code if it's wrapped in markdown code blocks
        if "```" in debugged_code:
            code_blocks = debugged_code.split("```")
            for i, block in enumerate(code_blocks):
                if i % 2 == 1:  # Odd-indexed blocks are code
                    if block.startswith(language):
                        debugged_code = block[len(language):].strip()
                    else:
                        debugged_code = block.strip()
                    break
        
        logger.info(f"Debugged code: {debugged_code[:100]}...")
        
        return debugged_code