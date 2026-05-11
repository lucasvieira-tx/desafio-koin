import pytest

from datetime import date
from src.utils.date_parser import parse_date, parse_date_optional

def test_parse_date_valid_formats():
    assert parse_date("2023-12-31") == date(2023, 12, 31)
    assert parse_date("31-12-2023") == date(2023, 12, 31)
    assert parse_date("12-31-2023") == date(2023, 12, 31)
    assert parse_date("31/12/2023") == date(2023, 12, 31)
    assert parse_date("2023/12/31") == date(2023, 12, 31)
    assert parse_date("12/31/2023") == date(2023, 12, 31)

def test_parse_date_invalid_format():
    with pytest.raises(ValueError):
        parse_date("2024.31.12")

def test_parse_date_optional_return_none():
    assert parse_date_optional(None) is None

def test_parse_date_optional_return_date():
    assert parse_date_optional("2023-12-31") == date(2023, 12, 31)
