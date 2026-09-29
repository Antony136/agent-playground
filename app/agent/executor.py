from typing import Any

from app.tools.registry import ToolRegistry


class ToolExecutionResult:
    def __init__(
        self,
        success: bool,
        result: Any = None,
        error: str | None = None,
    ):
        self.success = success
        self.result = result
        self.error = error

    def __repr__(self) -> str:
        return (
            f"ToolExecutionResult("
            f"success={self.success}, "
            f"result={self.result!r}, "
            f"error={self.error!r}"
            f")"
        )


class ToolExecutor:
    def __init__(self, registry: ToolRegistry):
        self.registry = registry

    def execute(
        self,
        tool_name: str,
        arguments: dict,
    ) -> ToolExecutionResult:

        # Step 1: Find the tool
        try:
            tool = self.registry.get(tool_name)
        except KeyError as error:
            return ToolExecutionResult(
                success=False,
                error=str(error),
            )

        # Step 2: Execute the tool
        try:
            result = tool.function(**arguments)

            return ToolExecutionResult(
                success=True,
                result=result,
            )

        except Exception as error:
            return ToolExecutionResult(
                success=False,
                error=str(error),
            )