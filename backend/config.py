from pydantic_settings import BaseSettings
from functools import lru_cache
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    # App settings
    app_name: str = "AI-Powered Multi-Agent Coding Assistant"
    environment: str = os.getenv("ENVIRONMENT", "development")
    
    # OpenAI API settings
    openai_api_key: str = os.getenv("OPENAI_API_KEY", "")
    openai_model: str = os.getenv("OPENAI_MODEL", "gpt-4o")
    
    # GitHub API settings
    github_token: str = os.getenv("GITHUB_TOKEN", "")
    github_repo: str = os.getenv("GITHUB_REPO", "")
    github_owner: str = os.getenv("GITHUB_OWNER", "")
    
    # RAG settings
    vector_db_path: str = os.getenv("VECTOR_DB_PATH", "./vector_db")
    
    # Agent settings
    max_iterations: int = int(os.getenv("MAX_ITERATIONS", "10"))
    debug_mode: bool = os.getenv("DEBUG_MODE", "False").lower() in ('true', '1', 't')
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

@lru_cache
def get_settings() -> Settings:
    """Create and cache settings."""
    return Settings()