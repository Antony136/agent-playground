from pydantic import BaseModel
from typing import Any


class ToolParameter(BaseModel):
    name: str
    type: str
    description: str
    required: bool = True


class ToolSchema(BaseModel):
    name: str
    description: str
    parameters: list[ToolParameter]