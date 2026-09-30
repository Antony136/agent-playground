from pathlib import Path


def list_files(directory: str) -> list[str]:
    path = Path(directory)

    if not path.exists():
        raise FileNotFoundError(f"Directory does not exist: {directory}")

    if not path.is_dir():
        raise ValueError(f"Not a directory: {directory}")

    return [
        item.name
        for item in path.iterdir()
        if item.is_file()
    ]


def read_file(file_path: str) -> str:
    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"File does not exist: {file_path}")

    if not path.is_file():
        raise ValueError(f"Not a file: {file_path}")

    return path.read_text(encoding="utf-8")


def write_file(file_path: str, content: str) -> str:
    path = Path(file_path).resolve()

    workspace = Path("agent_workspace").resolve()

    if workspace not in path.parents:
        raise PermissionError(
            "File modification is only allowed inside agent_workspace."
        )

    path.write_text(content, encoding="utf-8")

    return f"File written successfully: {file_path}"


def search_files(directory: str, query: str) -> list[str]:
    path = Path(directory)

    if not path.exists():
        raise FileNotFoundError(f"Directory does not exist: {directory}")

    if not path.is_dir():
        raise ValueError(f"Not a directory: {directory}")

    matches = []

    for file in path.rglob("*"):
        if not file.is_file():
            continue

        try:
            content = file.read_text(encoding="utf-8")

            if query.lower() in content.lower():
                matches.append(str(file))

        except (UnicodeDecodeError, PermissionError):
            continue

    return matches