import csv
from pathlib import Path

from uploader_app.config import TEXT_UPLOAD_LOG_FILE


LOG_PATH = Path(TEXT_UPLOAD_LOG_FILE)

LOG_HEADER = ["pecha_text_id", "text_type", "title", "language", "source_link"]


def _ensure_log_file() -> None:
    """
    Make sure the CSV log file exists and has a header row.
    """
    if not LOG_PATH.exists():
        LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
        with LOG_PATH.open("w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(LOG_HEADER)


def has_been_uploaded(pecha_text_id: str, text_type: str) -> bool:
    """
    Check if a text with the given ID and type has already been logged.

    The combination of (pecha_text_id, text_type) is treated as the unique key.
    """
    if not LOG_PATH.exists():
        return False

    with LOG_PATH.open("r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if (
                row.get("pecha_text_id") == pecha_text_id
                and row.get("text_type") == text_type
            ):
                return True

    return False


def log_uploaded_text(
    pecha_text_id: str,
    text_type: str,
    title: str | None = None,
    language: str | None = None,
    source_link: str | None = None,
) -> None:
    """
    Append a record of an uploaded text to the CSV log.
    """
    _ensure_log_file()

    with LOG_PATH.open("a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(
            [
                pecha_text_id,
                text_type,
                title or "",
                language or "",
                source_link or "",
            ]
        )


