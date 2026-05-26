import httpx
import streamlit as st

from frontend.components.chat_message import render_citations, render_confidence


def _upload_files(backend_url: str, files):
    """Upload files to backend and return results."""
    results = []
    for f in files:
        try:
            response = httpx.post(
                f"{backend_url}/api/upload",
                files={"file": (f.name, f.getvalue())},
                timeout=120.0,
            )
            if response.status_code == 200:
                data = response.json()
                results.append({"name": f.name, "id": data["document_id"], "success": True})
            else:
                detail = response.json().get("detail", "Upload failed")
                results.append({"name": f.name, "success": False, "error": detail})
        except Exception as e:
            results.append({"name": f.name, "success": False, "error": str(e)})
    return results


def render(backend_url: str):
    st.header("Chat with your documents")

    # Initialize state
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "uploaded_docs" not in st.session_state:
        st.session_state.uploaded_docs = []

    # Sidebar controls
    use_agents = st.sidebar.toggle(
        "Deep Analysis Mode", value=False,
        help="Use multi-agent system for deeper analysis",
    )

    # Sidebar: show uploaded documents
    if st.session_state.uploaded_docs:
        st.sidebar.markdown("---")
        st.sidebar.subheader(f"Documents ({len(st.session_state.uploaded_docs)})")
        for doc in st.session_state.uploaded_docs:
            st.sidebar.caption(f"{doc['name']}  ({doc['id'][:8]}...)")

    # File uploader inside chat area
    uploaded_files = st.file_uploader(
        "Upload documents to analyze",
        type=["pdf", "png", "jpg", "jpeg", "txt", "log", "json"],
        accept_multiple_files=True,
        key="chat_uploader",
        help="Upload files, then ask questions about them below",
    )

    # Process new uploads
    if uploaded_files:
        new_files = [
            f for f in uploaded_files
            if f.name not in {d["name"] for d in st.session_state.uploaded_docs}
        ]
        if new_files:
            with st.spinner(f"Uploading {len(new_files)} file(s)..."):
                results = _upload_files(backend_url, new_files)

            for r in results:
                if r["success"]:
                    st.session_state.uploaded_docs.append({"name": r["name"], "id": r["id"]})
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": f"Uploaded **{r['name']}** successfully. You can now ask questions about it.",
                    })
                else:
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": f"Failed to upload **{r['name']}**: {r['error']}",
                    })
            st.rerun()

    st.markdown("---")

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
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

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

                        st.session_state.messages.append({
                            "role": "assistant",
                            "content": result["answer"],
                            "citations": result.get("citations", []),
                            "confidence": result.get("confidence_score", 0),
                        })
                    else:
                        error = response.json().get("detail", "Unknown error")
                        st.error(f"Error: {error}")
                except httpx.ConnectError:
                    st.error("Cannot connect to backend. Is it running?")
                except Exception as e:
                    st.error(f"Error: {e}")
