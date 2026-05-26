import os
import tempfile

import pytest


@pytest.fixture
def sample_text_file(tmp_path):
    content = """ERROR 2024-01-15 10:23:45 - Application startup failed
Traceback (most recent call last):
  File "app.py", line 42, in start_server
    connection = db.connect(host="prod-db", port=5432)
  File "db.py", line 18, in connect
    raise ConnectionError("Connection refused")
ConnectionError: Connection refused

WARN 2024-01-15 10:23:46 - Retrying connection (attempt 2/3)
ERROR 2024-01-15 10:23:47 - Connection retry failed
INFO 2024-01-15 10:23:48 - Falling back to read replica
"""
    file_path = tmp_path / "sample_log.txt"
    file_path.write_text(content)
    return str(file_path)


@pytest.fixture
def sample_json_file(tmp_path):
    import json

    data = {
        "test_suite": "login_tests",
        "status": "failed",
        "total": 10,
        "passed": 7,
        "failed": 3,
        "failures": [
            {
                "test": "test_login_with_valid_credentials",
                "error": "TimeoutError: Element not found after 30s",
                "screenshot": "login_failure.png",
            },
            {
                "test": "test_password_reset",
                "error": "AssertionError: Expected 200, got 500",
                "screenshot": "reset_failure.png",
            },
            {
                "test": "test_oauth_redirect",
                "error": "URLError: Invalid redirect URI",
                "screenshot": None,
            },
        ],
    }
    file_path = tmp_path / "test_report.json"
    file_path.write_text(json.dumps(data))
    return str(file_path)


@pytest.fixture
def sample_pdf_file(tmp_path):
    """Create a minimal PDF for testing."""
    # Minimal valid PDF
    pdf_content = b"""%PDF-1.0
1 0 obj
<< /Type /Catalog /Pages 2 0 R >>
endobj
2 0 obj
<< /Type /Pages /Kids [3 0 R] /Count 1 >>
endobj
3 0 obj
<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] /Contents 4 0 R /Resources << /Font << /F1 5 0 R >> >> >>
endobj
4 0 obj
<< /Length 44 >>
stream
BT /F1 12 Tf 100 700 Td (Test PDF) Tj ET
endstream
endobj
5 0 obj
<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>
endobj
xref
0 6
0000000000 65535 f
0000000009 00000 n
0000000058 00000 n
0000000115 00000 n
0000000266 00000 n
0000000360 00000 n
trailer
<< /Size 6 /Root 1 0 R >>
startxref
441
%%EOF"""
    file_path = tmp_path / "sample.pdf"
    file_path.write_bytes(pdf_content)
    return str(file_path)
