from app.tools.calculator_schema import calculator_schema


def main():
    print("Tool name:")
    print(calculator_schema.name)

    print("\nDescription:")
    print(calculator_schema.description)

    print("\nParameters:")

    for parameter in calculator_schema.parameters:
        print(f"- {parameter.name}")
        print(f"  Type: {parameter.type}")
        print(f"  Description: {parameter.description}")
        print(f"  Required: {parameter.required}")


if __name__ == "__main__":
    main()