from ingestion.parsers.pdf_parser import parse_pdf


def test_parse_pdf_file(sample_pdf_file):
    result = parse_pdf(sample_pdf_file)

    assert result.metadata["source_type"] == "pdf"
    assert result.metadata["page_count"] == 1
    # The minimal PDF may or may not extract text depending on the reader
    assert isinstance(result.text, str)
