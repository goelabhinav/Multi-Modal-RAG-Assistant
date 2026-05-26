import streamlit as st


def render_citations(citations: list[dict]):
    if not citations:
        return

    with st.expander(f"Sources ({len(citations)})"):
        for c in citations:
            score_pct = round(c.get("score", 0) * 100, 1)
            st.markdown(
                f'<span class="citation-chip">'
                f'Doc: {c["document_id"][:8]}... | Chunk {c["chunk_index"]} | '
                f"Score: {score_pct}%"
                f"</span>",
                unsafe_allow_html=True,
            )
            st.caption(c.get("text", "")[:150] + "...")


def render_confidence(score: float):
    if score <= 0:
        return

    pct = round(score * 100)
    if score >= 0.7:
        level = "high"
        color = "#22c55e"
    elif score >= 0.4:
        level = "medium"
        color = "#f59e0b"
    else:
        level = "low"
        color = "#ef4444"

    st.markdown(
        f"""
        <div class="confidence-container">
            <small>Confidence: {pct}% ({level})</small>
            <div class="confidence-bar confidence-{level}" style="width: {pct}%"></div>
        </div>
        """,
        unsafe_allow_html=True,
    )
