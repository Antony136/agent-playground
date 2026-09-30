from app.tools.file_tools import write_file


def main():
    result = write_file(
        "agent_workspace/example.py",
        """def greet(name):
    return f"Hello, {name}!"

def farewell(name):
    return f"Goodbye, {name}!"
""",
    )

    print(result)


if __name__ == "__main__":
    main()