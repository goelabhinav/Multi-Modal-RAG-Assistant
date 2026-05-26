import logging
from dataclasses import dataclass, field

from ingestion.parsers.image_parser import parse_image
from ingestion.parsers.json_parser import parse_json
from ingestion.parsers.pdf_parser import parse_pdf
from ingestion.parsers.text_parser import parse_text

logger = logging.getLogger(__name__)


@dataclass
class IngestionResult:
    text: str
    metadata: dict = field(default_factory=dict)
    source_type: str = ""
    success: bool = True
    error: str = ""


PARSER_MAP = {
    "application/pdf": parse_pdf,
    "image/png": parse_image,
    "image/jpeg": parse_image,
    "text/plain": parse_text,
    "application/json": parse_json,
}


def ingest_document(file_path: str, mime_type: str) -> IngestionResult:
    parser = PARSER_MAP.get(mime_type)
    if not parser:
        return IngestionResult(
            text="",
            success=False,
            error=f"No parser for mime type: {mime_type}",
        )

    try:
        result = parser(file_path)
        return IngestionResult(
            text=result.text,
            metadata=result.metadata,
            source_type=mime_type,
            success=True,
        )
    except Exception as e:
        logger.exception("Failed to ingest document: %s", file_path)
        return IngestionResult(
            text="",
            success=False,
            error=str(e),
        )
