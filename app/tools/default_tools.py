from app.schemas.tool import ToolDefinition

from app.tools.calculator import calculator
from app.tools.calculator_schema import calculator_schema

from app.tools.file_tools import (
    list_files,
    read_file,
    write_file,
    search_files,
)

from app.tools.file_tool_schemas import (
    list_files_schema,
    read_file_schema,
    write_file_schema,
    search_files_schema,
)

from app.tools.registry import ToolRegistry


def create_tool_registry() -> ToolRegistry:
    registry = ToolRegistry()

    registry.register(
        ToolDefinition(
            schema=calculator_schema,
            function=calculator,
        )
    )

    registry.register(
        ToolDefinition(
            schema=list_files_schema,
            function=list_files,
        )
    )

    registry.register(
        ToolDefinition(
            schema=read_file_schema,
            function=read_file,
        )
    )

    registry.register(
        ToolDefinition(
            schema=write_file_schema,
            function=write_file,
        )
    )

    registry.register(
        ToolDefinition(
            schema=search_files_schema,
            function=search_files,
        )
    )

    return registry