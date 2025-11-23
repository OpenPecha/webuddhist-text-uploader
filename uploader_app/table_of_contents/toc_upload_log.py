import csv
from pathlib import Path
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
TOC_UPLOAD_LOG_FILE = os.path.join(BASE_DIR, "toc_upload_log.csv")
LOG_PATH = Path(TOC_UPLOAD_LOG_FILE)

# Header for TOC upload log: collection_id, pecha_collection_id, slug
LOG_HEADER = [
    "pecha_text_id",
    "id",
    "text_id"
]


def _ensure_log_file() -> None:
    """Ensure the log file exists with the proper header."""
    if not LOG_PATH.exists():
        LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
        with LOG_PATH.open("w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(LOG_HEADER)
        return

    # If the file exists, ensure its header matches the current LOG_HEADER.
    with LOG_PATH.open("r", newline="", encoding="utf-8") as f:
        lines = f.readlines()

    if not lines:
        # Empty file – just write the new header.
        with LOG_PATH.open("w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(LOG_HEADER)
        return

    # Parse the existing header row via csv to handle commas/quoting correctly.
    existing_header = next(csv.reader([lines[0].strip()]))

    if existing_header == LOG_HEADER:
        # Already up-to-date.
        return

    # If the header is different, we leave it alone to avoid data loss
    return


def is_toc_uploaded(pecha_text_id: str) -> bool:
    """
    Check if a TOC with the given pecha_text_id has already been uploaded.
    Returns True if found, False otherwise.
    """
    if not LOG_PATH.exists():
        return False

    with LOG_PATH.open("r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row.get("pecha_text_id") == pecha_text_id:
                return True

    return False


def log_uploaded_toc(
    pecha_text_id: str,
    id: str,
    text_id: str
) -> None:
    """
    Log an uploaded TOC with its pecha_text_id, id, and text_id.
    """
    _ensure_log_file()

    with LOG_PATH.open("a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(
            [
                pecha_text_id or "",
                id or "",
                text_id or "",
            ]
        )

