import streamlit as st
import httpx


def render_source_list(backend_url: str):
    try:
        response = httpx.get(f"{backend_url}/api/sources", timeout=10.0)
        if response.status_code != 200:
            st.warning("Could not load sources.")
            return

        sources = response.json()
        if not sources:
            st.info("No documents uploaded yet.")
            return

        st.subheader(f"Uploaded Documents ({len(sources)})")
        for doc in sources:
            status_icon = {"completed": "OK", "processing": "...", "failed": "X", "pending": "?"}
            icon = status_icon.get(doc["status"], "?")

            col1, col2, col3 = st.columns([3, 1, 1])
            with col1:
                st.text(doc["filename"])
            with col2:
                st.text(f"{doc['chunk_count']} chunks")
            with col3:
                st.text(f"[{icon}]")

    except httpx.ConnectError:
        st.warning("Backend not available.")
    except Exception as e:
        st.error(f"Error loading sources: {e}")
