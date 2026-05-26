from ingestion.parsers.image_parser import parse_image


def extract_text_from_image(image_path: str) -> str:
    result = parse_image(image_path)
    return result.text
