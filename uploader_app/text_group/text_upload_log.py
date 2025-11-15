import csv
from pathlib import Path

from uploader_app.config import TEXT_UPLOAD_LOG_FILE


LOG_PATH = Path(TEXT_UPLOAD_LOG_FILE)

# New header includes the destination (webuddhist) text ID, while keeping
# existing fields the same for backwards compatibility with readers that only
# care about `pecha_text_id` and `text_type`.
LOG_HEADER = [
    "pecha_text_id",
    "text_id",
    "text_type",
    "title",
    "language",
    "source_link",
]

# Old header used before text_id was tracked.
OLD_LOG_HEADER = ["pecha_text_id", "text_type", "title", "language", "source_link"]


def _ensure_log_file() -> None:
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

    if existing_header == OLD_LOG_HEADER:
        # Upgrade header in-place, keep existing rows as-is. Old rows will
        # simply have an empty `text_id` when read via DictReader.
        with LOG_PATH.open("w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(LOG_HEADER)
            f.writelines(lines[1:])
        return

    # If the header is something unexpected, leave it alone instead of
    # attempting a risky migration.
    return


def has_been_uploaded(pecha_text_id: str, text_type: str) -> bool:

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
    text_id: str | None = None,
    title: str | None = None,
    language: str | None = None,
    source_link: str | None = None,
) -> None:

    _ensure_log_file()

    with LOG_PATH.open("a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(
            [
                pecha_text_id,
                text_id or "",
                text_type,
                title or "",
                language or "",
                source_link or "",
            ]
        )


