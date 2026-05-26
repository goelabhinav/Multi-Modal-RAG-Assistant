QUERY_PROMPT = """You are a QA and incident investigation assistant. Use the provided context to answer the user's question accurately.

Rules:
1. Base your answer ONLY on the provided context.
2. If the context doesn't contain enough information, say so clearly.
3. Cite specific sources using [Source: document_id, chunk N] format.
4. Be concise but thorough.
5. If analyzing errors or incidents, identify patterns and suggest root causes.

Context:
{context}

Question: {question}

Answer:"""

INCIDENT_SUMMARY_PROMPT = """Based on the following documents and analysis, provide an incident summary.

Documents:
{context}

Provide:
1. A brief summary of the incident
2. Related documents and their relevance
3. Probable root causes (ranked by likelihood)
4. Recommended actions

Summary:"""

SCREENSHOT_ANALYSIS_PROMPT = """Analyze the following extracted content from a UI screenshot.

OCR and Visual Analysis:
{content}

Identify:
1. Any error messages or warnings visible
2. UI elements that appear broken or misaligned
3. The application state and context
4. Potential causes of the observed issue

Analysis:"""

LOG_ANALYSIS_PROMPT = """Analyze the following log content for issues and patterns.

Log Content:
{content}

Identify:
1. Error messages and their severity
2. Stack traces and their root causes
3. Patterns or recurring issues
4. Timeline of events
5. Affected components

Analysis:"""
