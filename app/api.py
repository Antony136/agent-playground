from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.agent.executor import ToolExecutor
from app.agent.loop import AgentLoop
from app.schemas.api import AgentRequest, AgentResponse
from app.tools.default_tools import create_tool_registry


app = FastAPI(
    title="AI Agent API",
    description="API for the AI Developer / Research Agent",
    version="1.0.0",
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


registry = create_tool_registry()
executor = ToolExecutor(registry)
agent = AgentLoop(executor)


@app.get("/")
def root():
    return {
        "message": "AI Agent API is running."
    }


@app.post("/agent", response_model=AgentResponse)
def run_agent(request: AgentRequest):
    answer = agent.run(request.request)

    return AgentResponse(
        answer=str(answer)
    )