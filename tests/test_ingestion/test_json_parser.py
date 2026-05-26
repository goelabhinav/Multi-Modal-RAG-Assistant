from ingestion.parsers.json_parser import parse_json


def test_parse_json_file(sample_json_file):
    result = parse_json(sample_json_file)

    assert result.text
    assert "test_suite" in result.text
    assert "login_tests" in result.text
    assert "TimeoutError" in result.text
    assert result.metadata["source_type"] == "json"
    assert "test_suite" in result.metadata["keys"]


def test_parse_simple_json(tmp_path):
    import json

    data = {"key": "value", "number": 42}
    file_path = tmp_path / "simple.json"
    file_path.write_text(json.dumps(data))

    result = parse_json(str(file_path))

    assert "key: value" in result.text
    assert "number: 42" in result.text
