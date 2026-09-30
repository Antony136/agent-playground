def search_knowledge_base(query: str) -> str:
    """
    Temporary RAG interface.

    This will later call the real RAG Document Q&A
    retrieval pipeline.
    """

    knowledge = {
        "rag": """
RAG stands for Retrieval-Augmented Generation.
It retrieves relevant information from an external
knowledge source and provides that information to
an LLM so it can generate a grounded answer.
""",
        "embedding": """
An embedding represents text as a numerical vector.
Similar pieces of text tend to have similar vectors,
which allows semantic similarity search.
""",
        "chunk": """
Chunking divides a document into smaller pieces before
creating embeddings and storing them for retrieval.
""",
    }

    query_lower = query.lower()

    results = []

    for keyword, content in knowledge.items():
        if keyword in query_lower:
            results.append(content.strip())

    if not results:
        return "No relevant information was found."

    return "\n\n".join(results)