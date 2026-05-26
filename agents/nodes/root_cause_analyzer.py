import logging

from agents.state import AgentState
from backend.services.llm_service import get_llm_service

logger = logging.getLogger(__name__)


async def root_cause_analyzer_node(state: AgentState) -> dict:
    """Determines probable root causes based on prior agent analysis."""
    llm = get_llm_service()
    query = state["query"]
    analysis_results = state.get("analysis_results", {})

    # Gather all previous analysis
    prior_analysis_parts = []
    for agent_name, result in analysis_results.items():
        if isinstance(result, dict) and "analysis" in result:
            prior_analysis_parts.append(f"[{agent_name}]\n{result['analysis']}")

    prior_analysis = "\n\n---\n\n".join(prior_analysis_parts)

    prompt = f"""Based on the following analysis from different investigation agents, determine the root cause(s).

Prior Analysis:
{prior_analysis}

Original Query: {query}

Provide:
1. Most probable root cause (with confidence level: high/medium/low)
2. Alternative possible causes
3. Evidence supporting each cause
4. Recommended next steps for investigation or remediation

Root Cause Analysis:"""

    analysis = await llm.generate(prompt)

    analysis_results["root_cause"] = {
        "analysis": analysis,
    }

    return {
        "analysis_results": analysis_results,
    }
