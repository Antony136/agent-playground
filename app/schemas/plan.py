from pydantic import BaseModel


class Plan(BaseModel):
    steps: list[str]