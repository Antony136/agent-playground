from datetime import datetime
from pydantic import BaseModel


class AgentEvent(BaseModel):
    event_type: str
    timestamp: datetime
    data: dict