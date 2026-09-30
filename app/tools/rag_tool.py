from app.rag_adapter import search_rag


def search_knowledge_base(query: str) -> str:
    """
    Search the real RAG Document Q&A knowledge base
    and return relevant retrieved context.
    """

    return search_rag(query)