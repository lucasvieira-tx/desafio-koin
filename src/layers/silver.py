from pathlib import Path
from typing import Any, Type

from pydantic import BaseModel, ValidationError

from src.utils.csv_io import read_csv, write_csv

REJECTED_FIELDS = ["rejection_layer", "rejection_reason", "row_number"]


"""
TODO:
1- Read bronze CSV and validate each row against the provided Pydantic schema
2- For rows that fail validation, add them to the rejected records with appropriate rejection reasons
3- For valid rows, apply deduplication based on the specified strategy
4- Write the valid deduplicated records to the silver CSV
5- Write the rejected records to the rejected CSV, ensuring all relevant fields are included
6- Return a summary of the processing results, including counts of total, valid, rejected, and deduplicated records
"""

class SilverProcessor:
    def process(
        self,
        bronze_path: Path,
        silver_path: Path,
        rejected_path: Path,
        schema: Type[BaseModel],
        primary_key: str,
        required_fields: list[str],
        deduplication: str,
    ) -> dict[str, int]:
        bronze_rows = list(read_csv(bronze_path))
        valid_records: list[dict[str, Any]] = []
        rejected_records: list[dict[str, Any]] = []

        for row_number, row in enumerate(bronze_rows, start=1):
            if row.get("is_valid", "false").lower() != "true":
                self._reject(rejected_records, row, "invalid_flag_false", row_number)
                continue

            missing_fields = [field for field in required_fields if not row.get(field)]
            if missing_fields:
                reason = f"missing_required_field:{','.join(missing_fields)}"
                self._reject(rejected_records, row, reason, row_number)
                continue

            try:
                parsed_record = schema.model_validate(row)
            except ValidationError as exc:
                self._reject(rejected_records, row, f"validation_error:{exc}", row_number)
                continue

            valid_records.append(
                {
                    "row_number": row_number,
                    "raw": row,
                    "data": parsed_record.model_dump(),
                }
            )

        if deduplication == "keep_last":
            deduped_records = self._deduplicate_keep_last(valid_records, primary_key)
        elif deduplication == "keep_first_reject_conflicting":
            deduped_records = self._deduplicate_keep_first_reject_conflicting(
                valid_records,
                primary_key,
                rejected_records,
            )
        else:
            raise ValueError(f"Unknown deduplication strategy: {deduplication}")

        silver_rows = [record["data"] for record in deduped_records]
        silver_fieldnames = list(schema.model_fields.keys())
        write_csv(silver_path, silver_rows, silver_fieldnames)

        rejected_fieldnames = self._rejected_fieldnames(bronze_rows, rejected_records)
        write_csv(rejected_path, rejected_records, rejected_fieldnames)

        return {
            "total_bronze": len(bronze_rows),
            "valid": len(silver_rows),
            "rejected": len(rejected_records),
            "deduped": len(valid_records) - len(silver_rows),
        }

    def _reject(
        self,
        rejected_records: list[dict[str, Any]],
        row: dict[str, Any],
        reason: str,
        row_number: int,
    ) -> None:
        normalized_reason = " | ".join(str(reason).splitlines())
        rejected_records.append(
            {
                **row,
                "rejection_layer": "silver",
                "rejection_reason": normalized_reason,
                "row_number": row_number,
            }
        )

    def _deduplicate_keep_last(
        self,
        records: list[dict[str, Any]],
        primary_key: str,
    ) -> list[dict[str, Any]]:
        deduped_by_key: dict[Any, dict[str, Any]] = {}

        for record in records:
            deduped_by_key[record["data"][primary_key]] = record

        return list(deduped_by_key.values())

    def _deduplicate_keep_first_reject_conflicting(
        self,
        records: list[dict[str, Any]],
        primary_key: str,
        rejected_records: list[dict[str, Any]],
    ) -> list[dict[str, Any]]:
        deduped_by_key: dict[Any, dict[str, Any]] = {}

        for record in records:
            key = record["data"][primary_key]
            existing_record = deduped_by_key.get(key)

            if existing_record is None:
                deduped_by_key[key] = record
                continue

            if record["data"] != existing_record["data"]:
                self._reject(
                    rejected_records,
                    record["raw"],
                    f"duplicate_conflicting_primary_key:{primary_key}={key}",
                    record["row_number"],
                )

        return list(deduped_by_key.values())

    def _rejected_fieldnames(
        self,
        bronze_rows: list[dict[str, Any]],
        rejected_records: list[dict[str, Any]],
    ) -> list[str]:
        source_fields = list(bronze_rows[0].keys()) if bronze_rows else []

        for rejected_record in rejected_records:
            for field in rejected_record:
                if field not in source_fields and field not in REJECTED_FIELDS:
                    source_fields.append(field)

        return source_fields + [field for field in REJECTED_FIELDS if field not in source_fields]
