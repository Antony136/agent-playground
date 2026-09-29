from app.schemas.tool import ToolParameter, ToolSchema


calculator_schema = ToolSchema(
    name="calculator",
    description="Perform arithmetic calculations on numbers.",
    parameters=[
        ToolParameter(
            name="operation",
            type="string",
            description="The arithmetic operation: add, subtract, multiply, or divide.",
        ),
        ToolParameter(
            name="numbers",
            type="array[number]",
            description="The numbers to use in the calculation.",
        ),
    ],
)