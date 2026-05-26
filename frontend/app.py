import os

import streamlit as st

from frontend.styles.theme import apply_dark_theme

BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")

st.set_page_config(
    page_title="Multi-Modal RAG Assistant",
    layout="wide",
    initial_sidebar_state="expanded",
)

apply_dark_theme()

st.title("Multi-Modal RAG Assistant")
st.caption("Upload documents and ask questions about incidents, logs, and screenshots.")

# Sidebar navigation
page = st.sidebar.radio("Navigation", ["Chat", "Upload Documents", "History"])

st.sidebar.markdown("---")
st.sidebar.caption(f"Backend: {BACKEND_URL}")

# Render selected page
if page == "Chat":
    from frontend.pages.chat import render
    render(BACKEND_URL)
elif page == "Upload Documents":
    from frontend.pages.upload import render
    render(BACKEND_URL)
elif page == "History":
    from frontend.pages.history import render
    render(BACKEND_URL)
