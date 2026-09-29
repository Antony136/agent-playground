from ollama import chat


MODEL = "qwen2.5-coder:7b"


def main():
    response = chat(
        model=MODEL,
        messages=[
            {
                "role": "user",
                "content": "Explain what an AI agent is in simple terms."
            }
        ],
    )

    print(response.message.content)


if __name__ == "__main__":
    main()