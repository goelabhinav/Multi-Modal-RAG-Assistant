from dataclasses import dataclass, field

from PyPDF2 import PdfReader


@dataclass
class ParseResult:
    text: str
    metadata: dict = field(default_factory=dict)


def parse_pdf(file_path: str) -> ParseResult:
    reader = PdfReader(file_path)
    pages_text = []
    for i, page in enumerate(reader.pages):
        text = page.extract_text()
        if text:
            pages_text.append(f"[Page {i + 1}]\n{text}")

    full_text = "\n\n".join(pages_text)
    return ParseResult(
        text=full_text,
        metadata={
            "page_count": len(reader.pages),
            "source_type": "pdf",
        },
    )
