from app.schemas.tool import ToolParameter, ToolSchema


list_files_schema = ToolSchema(
    name="list_files",
    description="List files inside a directory.",
    parameters=[
        ToolParameter(
            name="directory",
            type="string",
            description="The directory whose files should be listed.",
        ),
    ],
)


read_file_schema = ToolSchema(
    name="read_file",
    description="Read the contents of a text file.",
    parameters=[
        ToolParameter(
            name="file_path",
            type="string",
            description="Path of the file to read.",
        ),
    ],
)


write_file_schema = ToolSchema(
    name="write_file",
    description="Write text content to a file.",
    parameters=[
        ToolParameter(
            name="file_path",
            type="string",
            description="Path of the file to write.",
        ),
        ToolParameter(
            name="content",
            type="string",
            description="Content to write into the file.",
        ),
    ],
)


search_files_schema = ToolSchema(
    name="search_files",
    description="Search files recursively for text.",
    parameters=[
        ToolParameter(
            name="directory",
            type="string",
            description="Directory where the search should start.",
        ),
        ToolParameter(
            name="query",
            type="string",
            description="Text to search for.",
        ),
    ],
)