# from autogen import Agent

# class CodingAgent(Agent):
#     def __init__(self):
#         super().__init__("CodingAgent")

#     def run(self, prompt: str) -> str:
#         # Placeholder for code generation logic
#         return f"Generated code for: {prompt}"

import logging
from typing import Dict, Any, List
import autogen
from openai import OpenAI

from backend.services.rag import RAGService

# Configure logging
logger = logging.getLogger(__name__)

class CodingAgent:
    """Agent for generating code based on requirements."""
    
    def __init__(self, openai_api_key: str, openai_model: str, rag_service: RAGService):
        """
        Initialize the Coding Agent.
        
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
        
        logger.info("Coding Agent initialized")
    
    def _setup_agent(self):
        """Set up the AutoGen agent for code generation."""
        config_list = [
            {
                "model": self.openai_model,
                "api_key": self.openai_api_key,
            }
        ]
        
        # Create the AutoGen agent
        coding_agent = autogen.AssistantAgent(
            name="coding_agent",
            llm_config={"config_list": config_list},
            system_message="""
            You are an expert programmer who specializes in writing clean, efficient, and well-structured code.
            Your job is to:
            1. Write code that implements the specified requirements
            2. Follow best practices for the specific programming language
            3. Ensure the code is maintainable and readable
            4. Include appropriate error handling
            5. Document your code with comments explaining complex logic
            """
        )
        
        return coding_agent
    
    def generate_code(self, requirements: str, language: str) -> str:
        """
        Generate code based on the provided requirements.
        
        Args:
            requirements: Structured requirements specification
            language: Target programming language
            
        Returns:
            Generated code
        """
        logger.info(f"Generating {language} code based on requirements...")
        
        # Use RAG to retrieve relevant code patterns or libraries
        context = self.rag_service.retrieve(f"{language} code patterns for {requirements[:100]}")
        
        # Format requirements and context for the LLM
        messages = [
            {
                "role": "system", 
                "content": f"""
                You are an expert {language} programmer. Your task is to generate clean, efficient, 
                and well-structured code based on the given requirements.
                """
            },
            {
                "role": "user", 
                "content": f"""
                I need you to generate {language} code based on the following requirements:
                
                REQUIREMENTS:
                {requirements}
                
                {f'RELEVANT CODE PATTERNS: {context}' if context else ''}
                
                Please generate complete, working code that fully implements these requirements.
                Include appropriate error handling and comments explaining complex logic.
                Only respond with the code and necessary inline comments, without additional explanations.
                """
            }
        ]
        
        # Call the OpenAI API
        response = self.client.chat.completions.create(
            model=self.openai_model,
            messages=messages,
            temperature=0.2,
            max_tokens=4000
        )
        
        generated_code = response.choices[0].message.content
        
        # Extract code if it's wrapped in markdown code blocks
        if "```" in generated_code:
            code_blocks = generated_code.split("```")
            for i, block in enumerate(code_blocks):
                if i % 2 == 1:  # Odd-indexed blocks are code
                    if block.startswith(language):
                        generated_code = block[len(language):].strip()
                    else:
                        generated_code = block.strip()
                    break
        
        logger.info(f"Generated code: {generated_code[:100]}...")
        
        return generated_code