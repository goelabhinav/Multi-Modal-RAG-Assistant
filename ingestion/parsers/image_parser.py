import logging
from dataclasses import dataclass, field

import pytesseract
from PIL import Image

logger = logging.getLogger(__name__)


@dataclass
class ParseResult:
    text: str
    metadata: dict = field(default_factory=dict)


def parse_image(file_path: str) -> ParseResult:
    image = Image.open(file_path)

    # OCR extraction
    ocr_text = pytesseract.image_to_string(image)

    # Get OCR confidence data
    try:
        ocr_data = pytesseract.image_to_data(image, output_type=pytesseract.Output.DICT)
        confidences = [int(c) for c in ocr_data["conf"] if int(c) > 0]
        avg_confidence = sum(confidences) / len(confidences) if confidences else 0.0
    except Exception:
        avg_confidence = 0.0

    width, height = image.size

    return ParseResult(
        text=f"OCR Content:\n{ocr_text.strip()}",
        metadata={
            "source_type": "image",
            "image_width": width,
            "image_height": height,
            "ocr_confidence": round(avg_confidence, 2),
        },
    )


async def parse_image_with_vision(file_path: str, llm_service) -> ParseResult:
    """Parse image using both OCR and vision model for richer analysis."""
    base_result = parse_image(file_path)

    try:
        vision_prompt = (
            "Analyze this image. Describe what you see, including any error messages, "
            "UI elements, text content, warnings, or anomalies. Be specific and detailed."
        )
        vision_description = await llm_service.analyze_image(file_path, vision_prompt)
        base_result.text += f"\n\nVisual Analysis:\n{vision_description}"
        base_result.metadata["has_vision_analysis"] = True
    except Exception as e:
        logger.warning("Vision analysis failed, using OCR only: %s", e)
        base_result.metadata["has_vision_analysis"] = False

    return base_result
