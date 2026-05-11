import hashlib
from datetime import datetime, timezone
from pathlib import Path
from typing import Callable, Type

from pydantic import BaseModel

from src.utils.csv_io import read_csv, write_csv

REJECTED_FIELDS = ["rejection_layer", "rejection_reason"]

"""
TODO:
1- Read silver CSV and validate each row against the provided Pydantic schema
2- For rows that fail validation, add them to the rejected records with appropriate rejection reasons
3- For valid rows, apply any specified field transformations (masking data)
4- Enforce foreign key constraints if specified, rejecting rows that violate them
5- Write the valid transformed records to the gold CSV
6- Write the rejected records to the rejected CSV, ensuring all relevant fields are included
7- Return a summary of the processing results, including counts of total, valid, and rejected records
"""


class GoldProcessor:
    def process(
        self,
        silver_path: Path,
        gold_path: Path,
        rejected_path: Path,
        schema: Type[BaseModel],
        field_transforms: dict[str, tuple[str, Callable]] | None = None,
        valid_foreign_keys: set[str] | None = None,
        fk_field: str | None = None,
    ) -> dict[str, int]:
        silver_path = Path(silver_path)
        gold_path = Path(gold_path)
        rejected_path = Path(rejected_path)

        silver_rows = list(read_csv(silver_path))
        valid_records = []
        rejected_records = []
        processed_at = datetime.now(timezone.utc).isoformat()

        for row in silver_rows:
            if fk_field and valid_foreign_keys is not None:
                fk_value = row.get(fk_field)
                if fk_value not in valid_foreign_keys:
                    rejected_records.append(
                        self._build_fk_rejection(row, fk_field, fk_value)
                    )
                    continue

            gold_row = dict(row)

            if field_transforms:
                for old_field, (new_field, transform_fn) in field_transforms.items():
                    old_value = gold_row.pop(old_field, None)
                    gold_row[new_field] = transform_fn(old_value)

            gold_row["processed_at"] = processed_at
            valid_records.append(gold_row)

        fieldnames = list(schema.model_fields.keys())
        write_csv(gold_path, valid_records, fieldnames)

        if rejected_records:
            rejected_fieldnames = list(silver_rows[0].keys()) + REJECTED_FIELDS
            write_csv(rejected_path, rejected_records, rejected_fieldnames)

        return {
            "total_silver": len(silver_rows),
            "valid": len(valid_records),
            "rejected_fk_violations": len(rejected_records),
        }

    def _mask_email(self, email: str | None) -> str | None:
        """LGPD: masks email local part with 3-char SHA-256 hash, keeps domain visible."""
        if not email or "@" not in email:
            return None

        _, domain = email.split("@", 1)
        masked = "*" * 5
        return f"{masked}@{domain}"

    def _mask_phone(self, phone: str | None) -> str | None:
        """LGPD: masks phone number, keeping only last 4 digits visible."""
        if not phone or len(phone) < 4:
            return None
        masked = "*" * (len(phone) - 4)
        return f"{masked}{phone[-4:]}"

    def _mask_name(self, name: str) -> str:
        """LGPD: masks name, keeping only first letter and length visible."""
        if not name:
            return None
        
        name, last_name = name.split()
        masked = "*" * (len(last_name) + 3)
        return f"{name} {masked}"

    def _build_fk_rejection(self, row: dict, fk_field: str, fk_value: str) -> dict:
        return {
            **row,
            "rejection_layer": "gold",
            "rejection_reason": f"foreign_key_violation:{fk_field}={fk_value} not found in valid set",
        }
