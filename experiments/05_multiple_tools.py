from app.tools.calculator import calculator
from app.tools.file_tools import (
    list_files,
    read_file,
    write_file,
    search_files,
)


def main():
    print("=== Calculator ===")

    result = calculator(
        "multiply",
        [10, 20],
    )

    print(result)

    print("\n=== List Files ===")

    files = list_files("app/tools")

    for file in files:
        print(file)

    print("\n=== Write File ===")

    message = write_file(
        "experiments/test_agent_file.txt",
        "This file was created by our AI agent project.",
    )

    print(message)

    print("\n=== Read File ===")

    content = read_file(
        "experiments/test_agent_file.txt"
    )

    print(content)

    print("\n=== Search Files ===")

    matches = search_files(
        "app",
        "calculator",
    )

    for match in matches:
        print(match)


if __name__ == "__main__":
    main()