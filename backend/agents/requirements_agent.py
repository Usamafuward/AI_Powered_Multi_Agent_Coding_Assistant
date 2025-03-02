# from autogen import Agent

# class RequirementsAgent(Agent):
#     def __init__(self):
#         super().__init__("RequirementsAgent")

#     def run(self, prompt: str) -> str:
#         # Placeholder for requirements generation logic
#         return f"Generated requirements for: {prompt}"

import logging
from typing import Dict, Any, List
import autogen
from openai import OpenAI
from backend.services.rag import RAGService

# Configure logging
logger = logging.getLogger(__name__)

class RequirementsAgent:
    """Agent for processing requirements and breaking tasks into coding subtasks."""
    
    def __init__(self, openai_api_key: str, openai_model: str, rag_service: RAGService):
        """
        Initialize the Requirements Agent.
        
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
        
        logger.info("Requirements Agent initialized")
    
    def _setup_agent(self):
        """Set up the AutoGen agent for requirements processing."""
        config_list = [
            {
                "model": self.openai_model,
                "api_key": self.openai_api_key,
            }
        ]
        
        # Create the AutoGen agent
        requirements_agent = autogen.AssistantAgent(
            name="requirements_agent",
            llm_config={"config_list": config_list},
            system_message="""
            You are a requirements analyst who specializes in breaking down coding tasks.
            Your job is to:
            1. Understand user requirements for coding tasks
            2. Break down complex requirements into clear, specific coding subtasks
            3. Identify potential edge cases and requirements that need clarification
            4. Format the output as a structured requirements specification
            """
        )
        
        return requirements_agent
    
    def process_requirements(self, prompt: str) -> str:
        """
        Process user prompt into structured requirements.
        
        Args:
            prompt: User prompt describing the coding task
            
        Returns:
            Structured requirements specification
        """
        logger.info(f"Processing requirements from prompt: {prompt[:50]}...")
        
        # Use RAG to retrieve relevant context if available
        context = self.rag_service.retrieve(prompt)
        
        # Format context and prompt for the LLM
        messages = [
            {
                "role": "system", 
                "content": """
                You are a requirements analyst who specializes in breaking down coding tasks.
                Your job is to understand user requirements for coding tasks and break them down 
                into clear, specific coding subtasks.
                """
            },
            {
                "role": "user", 
                "content": f"""
                I need you to analyze the following user prompt and convert it into structured 
                coding requirements:
                
                USER PROMPT:
                {prompt}
                
                {f'RELEVANT CONTEXT FROM KNOWLEDGE BASE: {context}' if context else ''}
                
                Please provide a detailed breakdown with:
                1. Main objective
                2. Specific functional requirements
                3. Technical requirements (languages, libraries, etc.)
                4. Potential edge cases to handle
                5. Acceptance criteria
                
                Format your response as a structured requirements document.
                """
            }
        ]
        
        # Call the OpenAI API
        response = self.client.chat.completions.create(
            model=self.openai_model,
            messages=messages,
            temperature=0.1,
            max_tokens=2000
        )
        
        requirements = response.choices[0].message.content
        logger.info(f"Generated requirements: {requirements[:100]}...")
        
        return requirements