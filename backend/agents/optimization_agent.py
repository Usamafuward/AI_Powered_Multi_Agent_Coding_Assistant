# from autogen import Agent

# class OptimizationAgent(Agent):
#     def __init__(self):
#         super().__init__("OptimizationAgent")

#     def run(self, code: str) -> str:
#         # Placeholder for optimization logic
#         return f"Optimized code: {code}"

import logging
from typing import Dict, Any, List, Optional
import autogen
from openai import OpenAI

from backend.services.rag import RAGService

# Configure logging
logger = logging.getLogger(__name__)

class OptimizationAgent:
    """Agent for optimizing code."""
    
    def __init__(self, openai_api_key: str, openai_model: str, rag_service: RAGService):
        """
        Initialize the Optimization Agent.
        
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
        
        logger.info("Optimization Agent initialized")
    
    def _setup_agent(self):
        """Set up the AutoGen agent for code optimization."""
        config_list = [
            {
                "model": self.openai_model,
                "api_key": self.openai_api_key,
            }
        ]
        
        # Create the AutoGen agent
        optimization_agent = autogen.AssistantAgent(
            name="optimization_agent",
            llm_config={"config_list": config_list},
            system_message="""
            You are an expert code optimizer. You analyze code to:
            1. Improve time complexity and performance
            2. Reduce space complexity and memory usage
            3. Enhance code readability and maintainability
            4. Apply language-specific optimizations and best practices
            5. Refactor to make the code more efficient
            
            You maintain the functionality of the code while making it more efficient.
            """
        )
        
        return optimization_agent
    
    def optimize_code(self, code: str, language: str, optimization_target: str = "performance") -> str:
        """
        Optimize the provided code.
        
        Args:
            code: Code to optimize
            language: Programming language of the code
            optimization_target: Target of optimization (performance, memory, readability)
            
        Returns:
            Optimized code
        """
        logger.info(f"Optimizing {language} code for {optimization_target}: {code[:50]}...")
        
        # Use RAG to retrieve relevant optimization patterns
        context = self.rag_service.retrieve(f"{language} code optimization for {optimization_target}")
        
        # Format code and context for the LLM
        messages = [
            {
                "role": "system", 
                "content": f"""
                You are an expert {language} code optimizer. Your task is to optimize the given code
                focusing on {optimization_target} without changing its core functionality.
                """
            },
            {
                "role": "user", 
                "content": f"""
                I need you to optimize the following {language} code for {optimization_target}:
                
                ```{language}
                {code}
                ```
                
                {f'RELEVANT OPTIMIZATION PATTERNS: {context}' if context else ''}
                
                Please optimize the code following these guidelines:
                
                {'- Improve time complexity and algorithmic efficiency' if optimization_target == 'performance' else ''}
                {'- Reduce memory usage and optimize space complexity' if optimization_target == 'memory' else ''}
                {'- Enhance readability, maintainability, and code organization' if optimization_target == 'readability' else ''}
                
                Return the complete optimized code. Add comments explaining significant optimizations.
                Only respond with the code and necessary inline comments, without additional explanations.
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
        
        optimized_code = response.choices[0].message.content
        
        # Extract code if it's wrapped in markdown code blocks
        if "```" in optimized_code:
            code_blocks = optimized_code.split("```")
            for i, block in enumerate(code_blocks):
                if i % 2 == 1:  # Odd-indexed blocks are code
                    if block.startswith(language):
                        optimized_code = block[len(language):].strip()
                    else:
                        optimized_code = block.strip()
                    break
        
        logger.info(f"Optimized code: {optimized_code[:100]}...")
        
        return optimized_code