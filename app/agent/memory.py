class ShortTermMemory:
    def __init__(self):
        self.messages: list[dict] = []

    def add_message(self, role: str, content: str) -> None:
        self.messages.append(
            {
                "role": role,
                "content": content,
            }
        )

    def get_messages(self) -> list[dict]:
        return self.messages.copy()

    def clear(self) -> None:
        self.messages.clear()
