import streamlit as st


def apply_dark_theme():
    st.markdown(
        """
    <style>
    /* Dark mode overrides */
    .stApp {
        background-color: #0e1117;
        color: #fafafa;
    }

    /* Chat message styling */
    .chat-message {
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 0.5rem;
    }

    /* Citation chip */
    .citation-chip {
        display: inline-block;
        background: #1e293b;
        border: 1px solid #334155;
        border-radius: 4px;
        padding: 2px 8px;
        margin: 2px;
        font-size: 0.8em;
        color: #60a5fa;
    }

    /* Confidence bar */
    .confidence-container {
        margin-top: 0.5rem;
    }
    .confidence-bar {
        height: 6px;
        border-radius: 3px;
        margin-top: 4px;
    }
    .confidence-high { background: linear-gradient(90deg, #22c55e, #16a34a); }
    .confidence-medium { background: linear-gradient(90deg, #f59e0b, #d97706); }
    .confidence-low { background: linear-gradient(90deg, #ef4444, #dc2626); }

    /* Source panel */
    .source-panel {
        background: #1e293b;
        border: 1px solid #334155;
        border-radius: 8px;
        padding: 1rem;
        margin-top: 0.5rem;
    }

    /* Upload area */
    .upload-area {
        border: 2px dashed #334155;
        border-radius: 8px;
        padding: 2rem;
        text-align: center;
    }
    </style>
    """,
        unsafe_allow_html=True,
    )
