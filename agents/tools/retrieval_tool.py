from rag.retriever import get_retriever


def retrieve_relevant_chunks(query: str, top_k: int = 10) -> list[dict]:
    retriever = get_retriever()
    return retriever.retrieve(query, top_k=top_k)
