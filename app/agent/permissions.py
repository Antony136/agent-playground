class PermissionManager:
    def __init__(self):
        self.allowed_tools = {
            "calculator",
            "list_files",
            "read_file",
            "search_files",
        }

        self.approval_required_tools = {
            "write_file",
        }

    def check(self, tool_name: str) -> str:
        if tool_name in self.allowed_tools:
            return "allowed"

        if tool_name in self.approval_required_tools:
            return "approval_required"

        return "denied"