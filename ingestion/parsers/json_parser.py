import json
from dataclasses import dataclass, field


@dataclass
class ParseResult:
    text: str
    metadata: dict = field(default_factory=dict)


def parse_json(file_path: str) -> ParseResult:
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    # Flatten JSON into readable text
    text_parts = _flatten_json(data)
    full_text = "\n".join(text_parts)

    return ParseResult(
        text=full_text,
        metadata={
            "source_type": "json",
            "keys": list(data.keys()) if isinstance(data, dict) else [],
            "is_array": isinstance(data, list),
        },
    )


def _flatten_json(data, prefix: str = "") -> list[str]:
    parts = []
    if isinstance(data, dict):
        for key, value in data.items():
            full_key = f"{prefix}.{key}" if prefix else key
            if isinstance(value, (dict, list)):
                parts.extend(_flatten_json(value, full_key))
            else:
                parts.append(f"{full_key}: {value}")
    elif isinstance(data, list):
        for i, item in enumerate(data):
            parts.extend(_flatten_json(item, f"{prefix}[{i}]"))
    else:
        parts.append(f"{prefix}: {data}")
    return parts
