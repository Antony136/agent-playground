from app.agent.memory import ShortTermMemory


def main():
    memory = ShortTermMemory()

    memory.add_message(
        "user",
        "My name is Antony."
    )

    memory.add_message(
        "assistant",
        "Nice to meet you, Antony."
    )

    memory.add_message(
        "user",
        "I am learning AI agents."
    )

    print("Stored messages:")

    for message in memory.get_messages():
        print(f"{message['role']}: {message['content']}")

    print("\nClearing memory...")

    memory.clear()

    print("Messages after clearing:")
    print(memory.get_messages())


if __name__ == "__main__":
    main()