from fastapi import FastAPI
from backend.agents.coding_agent import CodingAgent
from backend.agents.debugging_agent import DebuggingAgent
from backend.agents.documentation_agent import DocumentationAgent
from backend.agents.optimization_agent import OptimizationAgent
from backend.agents.requirements_agent import RequirementsAgent

app = FastAPI()
coding_agent = CodingAgent()
debugging_agent = DebuggingAgent()
documentation_agent = DocumentationAgent()
optimization_agent = OptimizationAgent()
requirements_agent = RequirementsAgent()

@app.get("/generate_code")
async def generate_code(prompt: str):
    code = coding_agent.run(prompt)
    return {"code": code}

@app.get("/debug_code")
async def debug_code(code: str):
    debugged_code = debugging_agent.run(code)
    return {"debugged_code": debugged_code}

@app.get("/document_code")
async def document_code(code: str):
    documentation = documentation_agent.run(code)
    return {"documentation": documentation}

@app.get("/optimize_code")
async def optimize_code(code: str):
    optimized_code = OptimizationAgent().run(code)
    return {"optimized_code": optimized_code}

@app.get("/get_requirements")
async def get_requirements():
    requirements = RequirementsAgent().run()
    return {"requirements": requirements}



