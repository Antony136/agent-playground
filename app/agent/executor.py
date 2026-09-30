from typing import Any

from app.agent.permissions import PermissionManager
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

    def __repr__(self):
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
        self.permissions = PermissionManager()

    def execute(
        self,
        tool_name: str,
        arguments: dict,
    ) -> ToolExecutionResult:

        permission = self.permissions.check(tool_name)

        if permission == "denied":
            return ToolExecutionResult(
                success=False,
                error=f"Permission denied for tool: {tool_name}",
            )

        if permission == "approval_required":
            return ToolExecutionResult(
                success=False,
                error=f"Approval required for tool: {tool_name}",
            )

        try:
            tool = self.registry.get(tool_name)
        except KeyError as error:
            return ToolExecutionResult(
                success=False,
                error=str(error),
            )

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