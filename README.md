# AI-Powered Multi-Agent Coding Assistant 🚀

A collaborative system where AI agents assist with code generation, debugging, optimization, documentation, and GitHub integration. Built with FastAPI, AutoGen, and OpenAI.

![Architecture Diagram](https://via.placeholder.com/800x400.png?text=System+Architecture+Diagram)

## Features ✨

- **Multi-Agent Collaboration**:  
  - Requirements Analysis ➔ Code Generation ➔ Debugging ➔ Optimization ➔ Documentation
- **AI-Powered Workflows**:
  - Context-aware code generation using RAG (Retrieval-Augmented Generation)
  - Automated debugging and optimization suggestions
  - Style-specific documentation generation
- **GitHub Integration**:
  - Automated commits, branch management, and pull requests
  - AI-generated commit messages
- **REST API**:
  - Task-based asynchronous processing
  - Real-time progress tracking

## Technologies 🛠️

### Backend  
FastAPI | AutoGen | OpenAI GPT-4 | LangChain | FAISS (Vector DB)  

### Services  
GitHub API | Docker | Azure App Services  

### Utilities  
Retry mechanisms | Code sanitization | Execution monitoring | Error handling  

---

## Installation ⚙️

### 1. Clone Repository
```bash
git clone https://github.com/Usamafuward/AI_Powered_Multi_Agent_Coding_Assistant.git
cd AI_Powered_Multi_Agent_Coding_Assistant
```

### 2. Set Up Environment
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate  # Windows
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configuration
Create a `.env` file:
```ini
OPENAI_API_KEY=your_openai_key
GITHUB_TOKEN=your_github_token
GITHUB_REPO=your_repo
GITHUB_OWNER=your_username
ENVIRONMENT=development
```

---

## Usage 🖥️

### Start Server
```bash
uvicorn main:app --reload
```

### Example API Request
Generate Python code for a Fibonacci sequence:
```bash
curl -X POST "http://localhost:8000/api/generate-code" \
-H "Content-Type: application/json" \
-d '{
  "prompt": "Generate a Fibonacci sequence function",
  "language": "python"
}'
```

### Check Task Status
```bash
curl "http://localhost:8000/api/task/task_1"
```

## API Endpoints 📡

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/generate-code` | POST | Generate code from natural language |
| `/api/debug-code` | POST | Debug existing code |
| `/api/optimize-code` | POST | Optimize code performance |
| `/api/document-code` | POST | Add documentation |
| `/api/github-integration` | POST | Push code to GitHub |
| `/api/task/{task_id}` | GET | Check task status |

---

## Deployment 🚢

### Docker Setup Frontend
```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY ./frontend /app/frontend
COPY ./static /app/static

ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1

EXPOSE 8010

CMD ["uvicorn", "frontend.main:app", "--host", "0.0.0.0", "--port", "8010"]
```

### Docker Setup Backend
```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY ./backend /app/backend

ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1

EXPOSE 8011

CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8011"]
```

### Azure Deployment
- Build Docker image
- Push to Azure Container Registry
- Deploy to Azure App Service

---

## Contributing 🤝

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature`
3. Commit changes: `git commit -m 'Add awesome feature'`
4. Push to branch: `git push origin feature/your-feature`
5. Open a Pull Request

---

## License 📄

MIT License - See [LICENSE](LICENSE) for details.

