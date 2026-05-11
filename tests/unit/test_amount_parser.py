import pytest

from src.utils.amount_parser import parse_amount
from decimal import Decimal

def test_parse_amount_valid_formats():
    assert parse_amount("1,234.56") == Decimal("1234.56")
    assert parse_amount("1234.56") == Decimal("1234.56")
    assert parse_amount("  1,234.56  ") == Decimal("1234.56")
    assert parse_amount("-1,234.56") == Decimal("-1234.56")
    assert parse_amount("") is None
    assert parse_amount("   ") is None
    assert parse_amount(None) is None
    assert parse_amount("   ") is None
    assert parse_amount("   ") is None


def test_parse_amount_invalid_formats():
    assert parse_amount("abc") is None
    assert parse_amount("1,234.56.78") is None
    assert parse_amount("1,234,567.89.00") is None
    assert parse_amount("1,234.56abc") is None
