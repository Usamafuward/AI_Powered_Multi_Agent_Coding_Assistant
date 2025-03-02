# from fastapi import FastAPI
# from backend.agents.coding_agent import CodingAgent
# from backend.agents.debugging_agent import DebuggingAgent
# from backend.agents.documentation_agent import DocumentationAgent
# from backend.agents.optimization_agent import OptimizationAgent
# from backend.agents.requirements_agent import RequirementsAgent

# app = FastAPI()
# coding_agent = CodingAgent()
# debugging_agent = DebuggingAgent()
# documentation_agent = DocumentationAgent()
# optimization_agent = OptimizationAgent()
# requirements_agent = RequirementsAgent()

# @app.get("/generate_code")
# async def generate_code(prompt: str):
#     code = coding_agent.run(prompt)
#     return {"code": code}

# @app.get("/debug_code")
# async def debug_code(code: str):
#     debugged_code = debugging_agent.run(code)
#     return {"debugged_code": debugged_code}

# @app.get("/document_code")
# async def document_code(code: str):
#     documentation = documentation_agent.run(code)
#     return {"documentation": documentation}

# @app.get("/optimize_code")
# async def optimize_code(code: str):
#     optimized_code = OptimizationAgent().run(code)
#     return {"optimized_code": optimized_code}

# @app.get("/get_requirements")
# async def get_requirements():
#     requirements = RequirementsAgent().run()
#     return {"requirements": requirements}


from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import logging

from backend.api.router import router
from backend.config import Settings, get_settings

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup and shutdown events for the FastAPI application."""
    settings = get_settings()
    logger.info(f"Starting application in {settings.environment} mode")
    # Any startup operations would go here
    yield
    # Any cleanup operations would go here
    logger.info("Application shutting down")

# Initialize FastAPI app
app = FastAPI(
    title="AI-Powered Multi-Agent Coding Assistant",
    description="A system where multiple AI agents collaborate to assist developers in coding tasks",
    version="0.1.0",
    lifespan=lifespan,
)

# Setup CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Modify for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API router
app.include_router(router, prefix="/api")

# Root endpoint
@app.get("/")
async def root():
    """Root endpoint providing basic info about the API."""
    return {
        "message": "AI-Powered Multi-Agent Coding Assistant API",
        "docs": "/docs",
        "status": "operational"
    }
