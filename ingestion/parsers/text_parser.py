from dataclasses import dataclass, field


@dataclass
class ParseResult:
    text: str
    metadata: dict = field(default_factory=dict)


def parse_text(file_path: str) -> ParseResult:
    with open(file_path, "r", encoding="utf-8", errors="replace") as f:
        content = f.read()

    # Detect if it looks like a log file
    is_log = _detect_log_format(content)

    return ParseResult(
        text=content,
        metadata={
            "source_type": "log" if is_log else "text",
            "line_count": content.count("\n") + 1,
            "char_count": len(content),
        },
    )


def _detect_log_format(content: str) -> bool:
    log_indicators = [
        "ERROR",
        "WARN",
        "INFO",
        "DEBUG",
        "FATAL",
        "Exception",
        "Traceback",
        "at ",
        "Stack trace",
    ]
    first_lines = content[:2000]
    matches = sum(1 for indicator in log_indicators if indicator in first_lines)
    return matches >= 2
