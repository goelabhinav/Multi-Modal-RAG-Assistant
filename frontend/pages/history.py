import streamlit as st


def render(backend_url: str):
    st.header("Query History")

    if "messages" not in st.session_state or not st.session_state.messages:
        st.info("No queries yet. Go to Chat to start asking questions.")
        return

    # Show conversation history
    user_queries = [m for m in st.session_state.messages if m["role"] == "user"]
    st.subheader(f"Total queries: {len(user_queries)}")

    for i, msg in enumerate(st.session_state.messages):
        if msg["role"] == "user":
            with st.expander(f"Q: {msg['content'][:80]}...", expanded=False):
                st.markdown(f"**Query:** {msg['content']}")

                # Find the assistant response that follows
                idx = st.session_state.messages.index(msg)
                if idx + 1 < len(st.session_state.messages):
                    response = st.session_state.messages[idx + 1]
                    if response["role"] == "assistant":
                        st.markdown(f"**Response:** {response['content'][:500]}...")
                        if response.get("confidence"):
                            st.progress(response["confidence"])
                            st.caption(f"Confidence: {response['confidence']:.0%}")
