from pathlib import Path
from datetime import datetime, timezone
from typing import Type
from pydantic import BaseModel, ValidationError
from src.utils.csv_io import read_csv, write_csv

METADATA_FIELDS = ["ingestion_timestamp", "source_file", "row_number", "is_valid", "error_msg"]

"""
TODO: 
1- Read the CSV file 
2- For each row, validate it against the provided Pydantic schema
3- Write the row in a file with valid or invalid
"""

class BronzeProcessor:
    def process(self, source_path: Path, output_path: Path, schema: Type[BaseModel]) -> dict:
        data = read_csv(source_path)
        processed_data = []
        for i, row in enumerate(data, start=1):
            try:
                schema.model_validate(row)
                is_valid = "true"
                error_msg = ""
            except ValidationError as e:
                is_valid = "false"
                error_msg = str(e)
                
                
            # I create the metadata felds to facilitate the traceability the data
            processed_row = {
                **row,
                "ingestion_timestamp": datetime.now(timezone.utc).isoformat(),
                "source_file": source_path,
                "row_number": i,
                "is_valid": is_valid,
                "error_msg": error_msg
            }
            processed_data.append(processed_row)

        fieldnames = list(schema.model_fields.keys()) + METADATA_FIELDS
        write_csv(output_path, processed_data, fieldnames)

        valid = sum(1 for row in processed_data if row["is_valid"] == "true")
        invalid = sum(1 for row in processed_data if row["is_valid"] == "false")
        return {"total": len(processed_data), "valid": valid, "invalid": invalid}

