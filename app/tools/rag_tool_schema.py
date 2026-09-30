from app.schemas.tool import ToolParameter, ToolSchema


search_knowledge_base_schema = ToolSchema(
    name="search_knowledge_base",
    description="Search the knowledge base for relevant information.",
    parameters=[
        ToolParameter(
            name="query",
            type="string",
            description="The question or topic to search for.",
        ),
    ],
)