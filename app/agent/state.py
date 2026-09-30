from pydantic import BaseModel, Field


class AgentState(BaseModel):
    user_request: str

    messages: list[dict] = Field(default_factory=list)

    current_action: str | None = None

    tool_results: list[str] = Field(default_factory=list)

    iteration: int = 0