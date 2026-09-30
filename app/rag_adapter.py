import os
import sys
from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path

from dotenv import load_dotenv


RAG_PROJECT_PATH = Path(r"D:\Github\RAG-Document-QA")
RAG_FILE = RAG_PROJECT_PATH / "app" / "rag.py"
RAG_ENV_FILE = RAG_PROJECT_PATH / ".env"


def load_rag_module():
    # Load Project 2's environment variables.
    load_dotenv(RAG_ENV_FILE)

    spec = spec_from_file_location(
        "rag_document_qa_rag",
        RAG_FILE,
    )

    if spec is None or spec.loader is None:
        raise ImportError(
            f"Could not load RAG module from: {RAG_FILE}"
        )

    module = module_from_spec(spec)

    original_path = sys.path.copy()

    try:
        sys.path.insert(0, str(RAG_PROJECT_PATH))

        # Temporarily remove Project 3's "app" package
        # so Project 2 can resolve its own app.* imports.
        sys.modules.pop("app", None)

        spec.loader.exec_module(module)

    finally:
        sys.path[:] = original_path

    return module


def search_rag(query: str) -> str:
    rag = load_rag_module()

    question, context, results, has_context = rag.retrieve_context(
        question=query,
        conversation=[],
    )

    if not has_context or not context:
        return "No relevant information was found in the knowledge base."

    sources = []

    for result in results:
        sources.append(
            f"Document {result['document_id']} "
            f"| {result['source']} "
            f"| Page {result['page']} "
            f"| Chunk {result['chunk_index']}"
        )

    return (
        f"Retrieved context:\n\n"
        f"{context}\n\n"
        f"Sources:\n"
        + "\n".join(f"- {source}" for source in sources)
    )