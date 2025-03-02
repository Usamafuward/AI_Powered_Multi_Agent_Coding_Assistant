from fastapi import APIRouter, HTTPException, Depends, BackgroundTasks
from typing import List, Dict, Any, Optional
import logging

from backend.api.models import (
    GenerateCodeRequest, 
    GenerateCodeResponse,
    DebugCodeRequest,
    OptimizeCodeRequest,
    DocumentCodeRequest,
    TaskStatus,
    TaskResponse,
    GithubIntegrationRequest
)
from backend.agents.agent_registry import get_agent_registry
from backend.services.github import GitHubService

# Configure logging
logger = logging.getLogger(__name__)

# Create router
router = APIRouter(tags=["coding-assistant"])

# Task storage (in-memory for simplicity, would use a database in production)
tasks = {}

@router.post("/generate-code", response_model=TaskResponse)
async def generate_code(
    request: GenerateCodeRequest,
    background_tasks: BackgroundTasks
):
    """Generate code based on requirements."""
    task_id = f"task_{len(tasks) + 1}"
    tasks[task_id] = {"status": TaskStatus.PENDING, "result": None}
    
    def process_code_generation():
        try:
            registry = get_agent_registry()
            
            # Step 1: Process requirements
            requirements = registry.requirements_agent.process_requirements(request.prompt)
            logger.info(f"Processed requirements: {requirements[:100]}...")
            
            # Step 2: Generate code
            code = registry.coding_agent.generate_code(requirements, request.language)
            logger.info(f"Generated code: {code[:100]}...")
            
            # Step 3: Debug code if requested
            if request.debug:
                code = registry.debugging_agent.debug_code(code, request.language)
                logger.info("Code debugged")
            
            # Step 4: Optimize code if requested
            if request.optimize:
                code = registry.optimization_agent.optimize_code(code, request.language)
                logger.info("Code optimized")
            
            # Step 5: Document code if requested
            if request.document:
                code = registry.documentation_agent.document_code(code, request.language)
                logger.info("Code documented")
            
            tasks[task_id] = {
                "status": TaskStatus.COMPLETED,
                "result": {"code": code, "language": request.language}
            }
        except Exception as e:
            logger.error(f"Error in code generation: {str(e)}")
            tasks[task_id] = {
                "status": TaskStatus.FAILED,
                "result": {"error": str(e)}
            }
    
    background_tasks.add_task(process_code_generation)
    return {"task_id": task_id, "status": TaskStatus.PENDING}

@router.get("/task/{task_id}", response_model=Dict[str, Any])
async def get_task_status(task_id: str):
    """Get the status of a task."""
    if task_id not in tasks:
        raise HTTPException(status_code=404, detail="Task not found")
    return tasks[task_id]

@router.post("/debug-code", response_model=TaskResponse)
async def debug_code(
    request: DebugCodeRequest,
    background_tasks: BackgroundTasks
):
    """Debug provided code."""
    task_id = f"task_{len(tasks) + 1}"
    tasks[task_id] = {"status": TaskStatus.PENDING, "result": None}
    
    def process_debugging():
        try:
            registry = get_agent_registry()
            debugged_code = registry.debugging_agent.debug_code(
                request.code, 
                request.language
            )
            tasks[task_id] = {
                "status": TaskStatus.COMPLETED,
                "result": {"code": debugged_code, "language": request.language}
            }
        except Exception as e:
            logger.error(f"Error in debugging: {str(e)}")
            tasks[task_id] = {
                "status": TaskStatus.FAILED,
                "result": {"error": str(e)}
            }
    
    background_tasks.add_task(process_debugging)
    return {"task_id": task_id, "status": TaskStatus.PENDING}

@router.post("/optimize-code", response_model=TaskResponse)
async def optimize_code(
    request: OptimizeCodeRequest,
    background_tasks: BackgroundTasks
):
    """Optimize provided code."""
    task_id = f"task_{len(tasks) + 1}"
    tasks[task_id] = {"status": TaskStatus.PENDING, "result": None}
    
    def process_optimization():
        try:
            registry = get_agent_registry()
            optimized_code = registry.optimization_agent.optimize_code(
                request.code, 
                request.language,
                request.optimization_target
            )
            tasks[task_id] = {
                "status": TaskStatus.COMPLETED,
                "result": {"code": optimized_code, "language": request.language}
            }
        except Exception as e:
            logger.error(f"Error in optimization: {str(e)}")
            tasks[task_id] = {
                "status": TaskStatus.FAILED,
                "result": {"error": str(e)}
            }
    
    background_tasks.add_task(process_optimization)
    return {"task_id": task_id, "status": TaskStatus.PENDING}

@router.post("/document-code", response_model=TaskResponse)
async def document_code(
    request: DocumentCodeRequest,
    background_tasks: BackgroundTasks
):
    """Document provided code."""
    task_id = f"task_{len(tasks) + 1}"
    tasks[task_id] = {"status": TaskStatus.PENDING, "result": None}
    
    def process_documentation():
        try:
            registry = get_agent_registry()
            documented_code = registry.documentation_agent.document_code(
                request.code, 
                request.language,
                request.documentation_style
            )
            tasks[task_id] = {
                "status": TaskStatus.COMPLETED,
                "result": {"code": documented_code, "language": request.language}
            }
        except Exception as e:
            logger.error(f"Error in documentation: {str(e)}")
            tasks[task_id] = {
                "status": TaskStatus.FAILED,
                "result": {"error": str(e)}
            }
    
    background_tasks.add_task(process_documentation)
    return {"task_id": task_id, "status": TaskStatus.PENDING}

@router.post("/github-integration", response_model=TaskResponse)
async def github_integration(
    request: GithubIntegrationRequest,
    background_tasks: BackgroundTasks
):
    """Push code to GitHub repository."""
    task_id = f"task_{len(tasks) + 1}"
    tasks[task_id] = {"status": TaskStatus.PENDING, "result": None}
    
    def process_github_integration():
        try:
            github_service = GitHubService()
            result = github_service.commit_and_push(
                code=request.code,
                file_path=request.file_path,
                commit_message=request.commit_message,
                branch=request.branch
            )
            tasks[task_id] = {
                "status": TaskStatus.COMPLETED,
                "result": result
            }
        except Exception as e:
            logger.error(f"Error in GitHub integration: {str(e)}")
            tasks[task_id] = {
                "status": TaskStatus.FAILED,
                "result": {"error": str(e)}
            }
    
    background_tasks.add_task(process_github_integration)
    return {"task_id": task_id, "status": TaskStatus.PENDING}