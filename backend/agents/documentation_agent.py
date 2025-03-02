# from autogen import Agent

# class DocumentationAgent(Agent):
#     def __init__(self):
#         super().__init__("DocumentationAgent")
        
#     def run(self, code: str) -> str:
#         # Placeholder for documentation logic
#         return f"Documented code: {code}"

import logging
from typing import Dict, Any, List, Optional
import autogen
from openai import OpenAI

from backend.services.rag import RAGService

# Configure logging
logger = logging.getLogger(__name__)

class DocumentationAgent:
    """Agent for documenting code."""
    
    def __init__(self, openai_api_key: str, openai_model: str, rag_service: RAGService):
        """
        Initialize the Documentation Agent.
        
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
        
        logger.info("Documentation Agent initialized")
    
    def _setup_agent(self):
        """Set up the AutoGen agent for code documentation."""
        config_list = [
            {
                "model": self.openai_model,
                "api_key": self.openai_api_key,
            }
        ]
        
        # Create the AutoGen agent
        documentation_agent = autogen.AssistantAgent(
            name="documentation_agent",
            llm_config={"config_list": config_list},
            system_message="""
            You are an expert code documenter. Your job is to:
            1. Add clear and concise comments explaining complex logic
            2. Create function and class docstrings following language conventions
            3. Document parameters, return values, and exceptions
            4. Explain the purpose of modules, classes, and functions
            5. Ensure documentation follows the specified style guide
            
            You maintain the functionality of the code while adding appropriate documentation.
            """
        )
        
        return documentation_agent
    
    def document_code(self, code: str, language: str, documentation_style: str = "standard") -> str:
        """
        Document the provided code.
        
        Args:
            code: Code to document
            language: Programming language of the code
            documentation_style: Style of documentation (standard, javadoc, docstring)
            
        Returns:
            Documented code
        """
        logger.info(f"Documenting {language} code in {documentation_style} style: {code[:50]}...")
        
        # Map documentation style to language-specific conventions
        style_mapping = {
            "python": {
                "standard": "Google docstring style",
                "docstring": "NumPy/SciPy docstring style",
                "javadoc": "reStructuredText (Sphinx) style"
            },
            "javascript": {
                "standard": "JSDoc style",
                "docstring": "YUIDoc style",
                "javadoc": "JSDoc style"
            },
            "java": {
                "standard": "Javadoc style",
                "docstring": "Javadoc style",
                "javadoc": "Javadoc style"
            },
            # Add more language mappings as needed
        }
        
        # Get the appropriate documentation style for the language
        doc_style = style_mapping.get(language.lower(), {}).get(documentation_style.lower(), "standard style")
        
        # Use RAG to retrieve relevant documentation patterns
        context = self.rag_service.retrieve(f"{language} {doc_style} documentation examples")
        
        # Format code and context for the LLM
        messages = [
            {
                "role": "system", 
                "content": f"""
                You are an expert {language} code documenter. Your task is to add comprehensive
                documentation to the given code following {doc_style} conventions.
                """
            },
            {
                "role": "user", 
                "content": f"""
                I need you to document the following {language} code using {doc_style}:
                
                ```{language}
                {code}
                ```
                
                {f'RELEVANT DOCUMENTATION EXAMPLES: {context}' if context else ''}
                
                Please add:
                1. Module/file-level documentation
                2. Class and function docstrings with parameters, return values, and exceptions
                3. Inline comments for complex logic
                4. Follow {doc_style} conventions consistently
                
                Return the complete documented code.
                Only respond with the code and necessary inline comments/docstrings, without additional explanations.
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
        
        documented_code = response.choices[0].message.content
        
        # Extract code if it's wrapped in markdown code blocks
        if "```" in documented_code:
            code_blocks = documented_code.split("```")
            for i, block in enumerate(code_blocks):
                if i % 2 == 1:  # Odd-indexed blocks are code
                    if block.startswith(language):
                        documented_code = block[len(language):].strip()
                    else:
                        documented_code = block.strip()
                    break
        
        logger.info(f"Documented code: {documented_code[:100]}...")
        
        return documented_code