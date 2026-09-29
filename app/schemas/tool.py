from pydantic import BaseModel
from typing import Any, Callable


class ToolParameter(BaseModel):
    name: str
    type: str
    description: str
    required: bool = True


class ToolSchema(BaseModel):
    name: str
    description: str
    parameters: list[ToolParameter]


class ToolDefinition:
    def __init__(
        self,
        schema: ToolSchema,
        function: Callable[..., Any],
    ):
        self.schema = schema
        self.function = function

    @property
    def name(self) -> str:
        return self.schema.name