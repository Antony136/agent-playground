from pydantic import BaseModel


class AgentRequest(BaseModel):
    request: str


class AgentResponse(BaseModel):
    answer: str