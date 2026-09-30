from langchain_core.messages import HumanMessage, SystemMessage
from langchain_ollama import ChatOllama


llm = ChatOllama(
    model="qwen2.5-coder:7b",
    temperature=0,
)


messages = [
    SystemMessage(
        content="You are a helpful AI assistant."
    ),
    HumanMessage(
        content="What is Retrieval-Augmented Generation?"
    ),
]


response = llm.invoke(messages)

print(response.content)