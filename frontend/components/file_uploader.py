import streamlit as st
import httpx


def render_upload_widget(backend_url: str):
    uploaded_files = st.file_uploader(
        "Upload documents for analysis",
        type=["pdf", "png", "jpg", "jpeg", "txt", "log", "json"],
        accept_multiple_files=True,
        help="Supported: PDF, PNG, JPG, TXT, LOG, JSON (max 50MB each)",
    )

    if uploaded_files:
        for uploaded_file in uploaded_files:
            if uploaded_file.name not in st.session_state.get("uploaded_files", set()):
                with st.spinner(f"Processing {uploaded_file.name}..."):
                    try:
                        files = {"file": (uploaded_file.name, uploaded_file.getvalue())}
                        response = httpx.post(
                            f"{backend_url}/api/upload",
                            files=files,
                            timeout=120.0,
                        )

                        if response.status_code == 200:
                            result = response.json()
                            st.success(
                                f"Uploaded: {uploaded_file.name} "
                                f"(ID: {result['document_id'][:8]}...)"
                            )
                            if "uploaded_files" not in st.session_state:
                                st.session_state.uploaded_files = set()
                            st.session_state.uploaded_files.add(uploaded_file.name)
                        else:
                            st.error(f"Failed: {response.json().get('detail', 'Unknown error')}")
                    except httpx.ConnectError:
                        st.error("Cannot connect to backend. Is it running?")
                    except Exception as e:
                        st.error(f"Upload error: {e}")
