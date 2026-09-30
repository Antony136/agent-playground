from langchain_core.tools import tool


@tool
def calculator(operation: str, numbers: list[float]) -> float:
    """Perform a basic mathematical operation on a list of numbers."""

    if not numbers:
        raise ValueError("At least one number is required.")

    if operation == "add":
        return sum(numbers)

    if operation == "multiply":
        result = 1

        for number in numbers:
            result *= number

        return result

    if operation == "subtract":
        result = numbers[0]

        for number in numbers[1:]:
            result -= number

        return result

    if operation == "divide":
        result = numbers[0]

        for number in numbers[1:]:
            if number == 0:
                raise ValueError("Cannot divide by zero.")

            result /= number

        return result

    raise ValueError(
        f"Unsupported operation: {operation}"
    )


print(calculator.name)
print(calculator.description)
print(calculator.args_schema.model_json_schema())