from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
from enum import Enum

class TaskStatus(str, Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"

class GenerateCodeRequest(BaseModel):
    prompt: str = Field(..., description="User prompt describing the coding task")
    language: str = Field("python", description="Target programming language")
    debug: bool = Field(True, description="Whether to debug the generated code")
    optimize: bool = Field(True, description="Whether to optimize the generated code")
    document: bool = Field(True, description="Whether to document the generated code")

class GenerateCodeResponse(BaseModel):
    code: str = Field(..., description="Generated code")
    language: str = Field(..., description="Programming language of the code")
    
class DebugCodeRequest(BaseModel):
    code: str = Field(..., description="Code to debug")
    language: str = Field(..., description="Programming language of the code")
    error_messages: Optional[List[str]] = Field(None, description="Error messages if available")

class OptimizeCodeRequest(BaseModel):
    code: str = Field(..., description="Code to optimize")
    language: str = Field(..., description="Programming language of the code")
    optimization_target: Optional[str] = Field("performance", description="Target of optimization (performance, memory, readability)")

class DocumentCodeRequest(BaseModel):
    code: str = Field(..., description="Code to document")
    language: str = Field(..., description="Programming language of the code")
    documentation_style: Optional[str] = Field("standard", description="Style of documentation (standard, javadoc, docstring)")

class GithubIntegrationRequest(BaseModel):
    code: str = Field(..., description="Code to push to GitHub")
    file_path: str = Field(..., description="File path in the repository")
    commit_message: str = Field(..., description="Commit message")
    branch: str = Field("main", description="Branch to push to")

class TaskResponse(BaseModel):
    task_id: str = Field(..., description="Unique identifier for the task")
    status: TaskStatus = Field(..., description="Current status of the task")