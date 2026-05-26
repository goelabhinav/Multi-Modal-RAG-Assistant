from typing import Annotated, Any

from langgraph.graph.message import add_messages
from typing_extensions import TypedDict


class AgentState(TypedDict):
    messages: Annotated[list, add_messages]
    query: str
    query_type: str  # "screenshot", "log", "incident", "general"
    documents: list[dict]  # Retrieved document chunks
    analysis_results: dict[str, Any]  # Results from each agent
    final_response: str
    citations: list[dict]
    confidence_score: float
    metadata: dict[str, Any]  # Latency, token usage, etc.
