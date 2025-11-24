import csv
from pathlib import Path

from uploader_app.config import TEXT_UPLOAD_LOG_FILE


LOG_PATH = Path(TEXT_UPLOAD_LOG_FILE)

# New header includes the destination (webuddhist) text ID, while keeping
# existing fields the same for backwards compatibility with readers that only
# care about `pecha_text_id` and `text_type`.
LOG_HEADER = [
    "instance_id",
    "pecha_text_id",
    "text_id",
    "text_type",
    "title",
    "language",
    "source_link",
    "category_id",
    "version_group_id",
    "log_group_id",
]

# Old header used before text_id was tracked.
OLD_LOG_HEADER = ["pecha_text_id", "text_type", "title", "language", "source_link"]

# Previous header before category_id and version_group_id were added
PREVIOUS_LOG_HEADER = [
    "pecha_text_id",
    "text_id",
    "text_type",
    "title",
    "language",
    "source_link",
]

# Header before log_group_id was added
BEFORE_LOG_GROUP_HEADER = [
    "pecha_text_id",
    "text_id",
    "text_type",
    "title",
    "language",
    "source_link",
    "category_id",
    "version_group_id",
]


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
        # simply have empty `text_id`, `category_id`, and `version_group_id` when read via DictReader.
        with LOG_PATH.open("w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(LOG_HEADER)
            f.writelines(lines[1:])
        return

    if existing_header == PREVIOUS_LOG_HEADER:
        # Upgrade from previous header to current one
        with LOG_PATH.open("w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(LOG_HEADER)
            f.writelines(lines[1:])
        return

    if existing_header == BEFORE_LOG_GROUP_HEADER:
        # Upgrade from before log_group_id header to current one
        with LOG_PATH.open("w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(LOG_HEADER)
            f.writelines(lines[1:])
        return

    # If the header is something unexpected, leave it alone instead of
    # attempting a risky migration.
    return


def has_been_uploaded_by_instance_id(instance_id: str, text_type: str) -> bool:

    if not LOG_PATH.exists():
        return False

    with LOG_PATH.open("r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if (
                row.get("instance_id") == instance_id
                and row.get("text_type") == text_type
            ):
                return True

    return False


def has_been_uploaded_by_pecha_text_id(pecha_text_id: str) -> bool:
    """
    Check if a text with the given pecha_text_id has already been uploaded.
    Returns True if the pecha_text_id exists in the upload log, False otherwise.
    """
    if not LOG_PATH.exists():
        return False

    with LOG_PATH.open("r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Check both 'pecha_text_id' and 'pecha' columns for compatibility
            if row.get("pecha_text_id") == pecha_text_id or row.get("pecha") == pecha_text_id:
                return True

    return False


def get_log_group_id_by_pecha_text_id(pecha_text_id: str) -> str | None:
    """
    Get the log_group_id for a given pecha_text_id from the upload log.
    Returns the log_group_id if found, None otherwise.
    """
    if not LOG_PATH.exists():
        return None

    with LOG_PATH.open("r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Check both 'pecha_text_id' and 'pecha' columns for compatibility
            if (row.get("pecha_text_id") == pecha_text_id):
                log_group_id = row.get("log_group_id")
                if log_group_id:
                    return log_group_id

    return None


def has_title_been_uploaded(title: str) -> bool:
    """
    Check if a text with the given title has already been uploaded.
    Returns True if the title exists in the upload log, False otherwise.
    """
    if not LOG_PATH.exists():
        return False

    with LOG_PATH.open("r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row.get("title") == title:
                return True

    return False


def get_version_group_id_by_category_id(category_id: str) -> str | None:
    """
    Look up version_group_id from the CSV by matching category_id.
    Returns the first matching version_group_id, or None if not found.
    """
    if not LOG_PATH.exists():
        return None

    with LOG_PATH.open("r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row.get("category_id") == category_id and row.get("version_group_id"):
                return row.get("version_group_id")

    return None


def get_version_group_id_by_log_group_and_category(log_group_id: str, category_id: str) -> str | None:
    """
    Look up version_group_id from the CSV by matching both log_group_id and category_id.
    Returns the first matching version_group_id, or None if not found.
    """
    if not LOG_PATH.exists():
        return None

    with LOG_PATH.open("r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if (row.get("log_group_id") == log_group_id and 
                row.get("category_id") == category_id and 
                row.get("version_group_id")):
                return row.get("version_group_id")

    return None


def log_uploaded_text(
    instance_id: str,
    pecha_text_id: str,
    text_type: str,
    text_id: str | None = None,
    title: str | None = None,
    language: str | None = None,
    source_link: str | None = None,
    category_id: str | None = None,
    version_group_id: str | None = None,
    log_group_id: str | None = None,
) -> None:

    _ensure_log_file()

    with LOG_PATH.open("a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(
            [
                instance_id,
                pecha_text_id,
                text_id or "",
                text_type,
                title or "",
                language or "",
                source_link or "",
                category_id or "",
                version_group_id or "",
                log_group_id or "",
            ]
        )


