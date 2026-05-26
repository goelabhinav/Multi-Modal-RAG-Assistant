from ingestion.validators import validate_file


def test_valid_pdf():
    result = validate_file("report.pdf", 1024)
    assert result.valid
    assert result.mime_type == "application/pdf"


def test_valid_png():
    result = validate_file("screenshot.png", 2048)
    assert result.valid
    assert result.mime_type == "image/png"


def test_valid_json():
    result = validate_file("report.json", 512)
    assert result.valid
    assert result.mime_type == "application/json"


def test_valid_txt():
    result = validate_file("log.txt", 4096)
    assert result.valid
    assert result.mime_type == "text/plain"


def test_valid_log():
    result = validate_file("output.log", 4096)
    assert result.valid
    assert result.mime_type == "text/plain"


def test_unsupported_extension():
    result = validate_file("malware.exe", 1024)
    assert not result.valid
    assert "Unsupported" in result.error


def test_file_too_large():
    huge_size = 100 * 1024 * 1024  # 100MB
    result = validate_file("big.pdf", huge_size)
    assert not result.valid
    assert "limit" in result.error


def test_no_extension():
    result = validate_file("noext", 1024)
    assert not result.valid
