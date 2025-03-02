from functools import lru_cache
import logging

from backend.agents.requirements_agent import RequirementsAgent
from backend.agents.coding_agent import CodingAgent
from backend.agents.debugging_agent import DebuggingAgent
from backend.agents.optimization_agent import OptimizationAgent
from backend.agents.documentation_agent import DocumentationAgent
from backend.config import get_settings
from backend.services.rag import RAGService

# Configure logging
logger = logging.getLogger(__name__)

class AgentRegistry:
    """Registry for managing all agent instances."""
    
    def __init__(self):
        """Initialize agent registry with all agent types."""
        logger.info("Initializing Agent Registry")
        
        # Initialize services
        self.settings = get_settings()
        self.rag_service = RAGService(vector_db_path=self.settings.vector_db_path)
        
        # Initialize agents
        self.requirements_agent = RequirementsAgent(
            openai_api_key=self.settings.openai_api_key,
            openai_model=self.settings.openai_model,
            rag_service=self.rag_service
        )
        
        self.coding_agent = CodingAgent(
            openai_api_key=self.settings.openai_api_key,
            openai_model=self.settings.openai_model,
            rag_service=self.rag_service
        )
        
        self.debugging_agent = DebuggingAgent(
            openai_api_key=self.settings.openai_api_key,
            openai_model=self.settings.openai_model,
            rag_service=self.rag_service
        )
        
        self.optimization_agent = OptimizationAgent(
            openai_api_key=self.settings.openai_api_key,
            openai_model=self.settings.openai_model,
            rag_service=self.rag_service
        )
        
        self.documentation_agent = DocumentationAgent(
            openai_api_key=self.settings.openai_api_key,
            openai_model=self.settings.openai_model,
            rag_service=self.rag_service
        )
        
        logger.info("Agent Registry initialized successfully")

@lru_cache
def get_agent_registry() -> AgentRegistry:
    """Create and cache the agent registry."""
    return AgentRegistry()