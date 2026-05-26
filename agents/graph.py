import logging

from langgraph.graph import END, StateGraph

from agents.nodes.incident_correlator import incident_correlator_node
from agents.nodes.log_analyzer import log_analyzer_node
from agents.nodes.report_generator import report_generator_node
from agents.nodes.root_cause_analyzer import root_cause_analyzer_node
from agents.nodes.screenshot_analyzer import screenshot_analyzer_node
from agents.state import AgentState
from backend.services.llm_service import get_llm_service

logger = logging.getLogger(__name__)


async def router_node(state: AgentState) -> dict:
    """Classify the query and route to the appropriate agent."""
    llm = get_llm_service()
    query = state["query"]
    query_type = await llm.classify_query(query)
    return {"query_type": query_type}


def route_by_query_type(state: AgentState) -> str:
    query_type = state.get("query_type", "general")
    if query_type == "screenshot":
        return "screenshot_analyzer"
    elif query_type == "log":
        return "log_analyzer"
    elif query_type == "incident":
        return "incident_correlator"
    else:
        return "report_generator"


def build_agent_graph() -> StateGraph:
    workflow = StateGraph(AgentState)

    # Add nodes
    workflow.add_node("router", router_node)
    workflow.add_node("screenshot_analyzer", screenshot_analyzer_node)
    workflow.add_node("log_analyzer", log_analyzer_node)
    workflow.add_node("incident_correlator", incident_correlator_node)
    workflow.add_node("root_cause_analyzer", root_cause_analyzer_node)
    workflow.add_node("report_generator", report_generator_node)

    # Entry point
    workflow.set_entry_point("router")

    # Conditional routing from router
    workflow.add_conditional_edges(
        "router",
        route_by_query_type,
        {
            "screenshot_analyzer": "screenshot_analyzer",
            "log_analyzer": "log_analyzer",
            "incident_correlator": "incident_correlator",
            "report_generator": "report_generator",
        },
    )

    # After specialized analysis, go to next step
    workflow.add_edge("screenshot_analyzer", "report_generator")
    workflow.add_edge("log_analyzer", "root_cause_analyzer")
    workflow.add_edge("incident_correlator", "root_cause_analyzer")
    workflow.add_edge("root_cause_analyzer", "report_generator")
    workflow.add_edge("report_generator", END)

    return workflow.compile()


# Singleton compiled graph
_agent_graph = None


def get_agent_graph():
    global _agent_graph
    if _agent_graph is None:
        _agent_graph = build_agent_graph()
    return _agent_graph
