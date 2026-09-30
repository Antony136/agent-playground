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

from app.tools.api_tools import get_exchange_rate
from app.tools.api_tool_schemas import exchange_rate_schema

from app.tools.rag_tool import search_knowledge_base
from app.tools.rag_tool_schema import search_knowledge_base_schema

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

    registry.register(
        ToolDefinition(
            schema=exchange_rate_schema,
            function=get_exchange_rate,
        )
    )

    registry.register(
        ToolDefinition(
            schema=search_knowledge_base_schema,
            function=search_knowledge_base,
        )
    )
    
    return registry