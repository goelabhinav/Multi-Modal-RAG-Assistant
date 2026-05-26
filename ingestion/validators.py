from dataclasses import dataclass

from backend.config import settings

ALLOWED_MIME_TYPES = {
    "application/pdf",
    "image/png",
    "image/jpeg",
    "text/plain",
    "application/json",
}

EXTENSION_TO_MIME = {
    ".pdf": "application/pdf",
    ".png": "image/png",
    ".jpg": "image/jpeg",
    ".jpeg": "image/jpeg",
    ".txt": "text/plain",
    ".log": "text/plain",
    ".json": "application/json",
}


@dataclass
class ValidationResult:
    valid: bool
    mime_type: str = ""
    error: str = ""


def validate_file(filename: str, file_size: int) -> ValidationResult:
    max_size = settings.MAX_UPLOAD_SIZE_MB * 1024 * 1024
    if file_size > max_size:
        return ValidationResult(
            valid=False, error=f"File exceeds {settings.MAX_UPLOAD_SIZE_MB}MB limit"
        )

    ext = _get_extension(filename)
    mime_type = EXTENSION_TO_MIME.get(ext, "")

    if not mime_type or mime_type not in ALLOWED_MIME_TYPES:
        return ValidationResult(valid=False, error=f"Unsupported file type: {ext}")

    return ValidationResult(valid=True, mime_type=mime_type)


def _get_extension(filename: str) -> str:
    if "." not in filename:
        return ""
    return "." + filename.rsplit(".", 1)[-1].lower()
