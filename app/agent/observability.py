from app.agent.events import AgentEvent
from datetime import datetime


class AgentTracer:
    def __init__(self):
        self.events: list[AgentEvent] = []

    def record(self, event_type: str, data: dict) -> None:
        event = AgentEvent(
            event_type=event_type,
            timestamp=datetime.now(),
            data=data,
        )

        self.events.append(event)

    def get_events(self) -> list[AgentEvent]:
        return self.events.copy()

    def clear(self) -> None:
        self.events.clear()