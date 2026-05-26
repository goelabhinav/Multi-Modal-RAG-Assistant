import httpx
import streamlit as st

from frontend.components.chat_message import render_citations, render_confidence


def render(backend_url: str):
    st.header("Chat with your documents")

    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Analysis mode toggle
    use_agents = st.sidebar.toggle("Deep Analysis Mode", value=False, help="Use multi-agent system for deeper analysis")

    # Display chat history
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
            if msg.get("citations"):
                render_citations(msg["citations"])
            if msg.get("confidence"):
                render_confidence(msg["confidence"])

    # Chat input
    if prompt := st.chat_input("Ask about your documents..."):
        # Show user message
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Get response from backend
        with st.chat_message("assistant"):
            with st.spinner("Analyzing..."):
                try:
                    endpoint = "/api/incidents/analyze" if use_agents else "/api/query"
                    response = httpx.post(
                        f"{backend_url}{endpoint}",
                        json={"query": prompt},
                        timeout=120.0,
                    )

                    if response.status_code == 200:
                        result = response.json()
                        st.markdown(result["answer"])
                        render_citations(result.get("citations", []))
                        render_confidence(result.get("confidence_score", 0))

                        st.caption(f"Latency: {result.get('latency_ms', 0):.0f}ms")

                        st.session_state.messages.append(
                            {
                                "role": "assistant",
                                "content": result["answer"],
                                "citations": result.get("citations", []),
                                "confidence": result.get("confidence_score", 0),
                            }
                        )
                    else:
                        error = response.json().get("detail", "Unknown error")
                        st.error(f"Error: {error}")
                except httpx.ConnectError:
                    st.error("Cannot connect to backend. Is it running?")
                except Exception as e:
                    st.error(f"Error: {e}")
