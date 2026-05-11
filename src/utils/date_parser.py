from datetime import datetime, date
from typing import Optional

DATE_FORMATS = ["%Y-%m-%d", "%d-%m-%Y", "%m-%d-%Y", "%d/%m/%Y", "%Y/%m/%d", "%m/%d/%Y"]

def parse_date(raw: str) -> date:
    """Parses a date string into a date object using predefined formats.
    Args:
        raw (str): The date string to parse. Leading and trailing whitespace is stripped.
    Returns:
        date: The parsed date object.
    Raises:
        ValueError: If the date string does not match any of the recognized formats.
    """
    
    for date in DATE_FORMATS:
        try:
            raw = raw.strip()
            return datetime.strptime(raw, date).date()
        except ValueError:
            continue
    raise ValueError(f"Date '{raw}' is not in a recognized format.")

def parse_date_optional(raw: Optional[str]) -> Optional[date]:
    """Parses an optional date string into a date object.

    If raw is None or an empty/whitespace-only string, returns None.
    Otherwise attempts to parse the string using parse_date and returns
    the resulting date object. Raises the same ValueError as parse_date
    when the string does not match any supported formats.

    Args:
        raw: An optional string containing the date to parse.

    Returns:
        A date object if parsing succeeds, or None if raw is None or empty.
    """
    if raw is None or raw.strip() == "":
        return None
    return parse_date(raw)