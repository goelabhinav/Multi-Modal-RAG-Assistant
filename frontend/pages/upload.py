import streamlit as st

from frontend.components.file_uploader import render_upload_widget
from frontend.components.source_viewer import render_source_list


def render(backend_url: str):
    st.header("Upload Documents")
    st.markdown("Upload documents for analysis. Supported formats: PDF, PNG, JPG, TXT, LOG, JSON.")

    render_upload_widget(backend_url)

    st.markdown("---")

    render_source_list(backend_url)
