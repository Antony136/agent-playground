from app.schemas.tool import ToolParameter, ToolSchema


exchange_rate_schema = ToolSchema(
    name="get_exchange_rate",
    description="Get the exchange rate between two currencies.",
    parameters=[
        ToolParameter(
            name="base_currency",
            type="string",
            description="The currency to convert from, such as USD.",
        ),
        ToolParameter(
            name="target_currency",
            type="string",
            description="The currency to convert to, such as EUR.",
        ),
    ],
)