from ingestion.parsers.text_parser import parse_text


def test_parse_text_file(sample_text_file):
    result = parse_text(sample_text_file)

    assert result.text
    assert "ERROR" in result.text
    assert "ConnectionError" in result.text
    assert result.metadata["source_type"] == "log"
    assert result.metadata["line_count"] > 0


def test_parse_regular_text(tmp_path):
    file_path = tmp_path / "readme.txt"
    file_path.write_text("This is a regular text file with no log patterns.")

    result = parse_text(str(file_path))

    assert result.text == "This is a regular text file with no log patterns."
    assert result.metadata["source_type"] == "text"
