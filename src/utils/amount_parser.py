from decimal import Decimal, InvalidOperation
from typing import Optional

def parse_amount(raw: str) -> Optional[Decimal]:
    """
    Parses a string representing an amount of money and returns it as a Decimal.
    
    Args:
        raw (str): The string to parse, e.g. "1,234.56" or "1234.56".
    
    Returns:
        Optional[Decimal]: The parsed amount as a Decimal, or None if parsing fails.
    """
    if raw is None:
        return None

    try:
        cleaned_amount = raw.replace(',', '').strip()
        return Decimal(cleaned_amount)
    except (InvalidOperation, ValueError):
        return None