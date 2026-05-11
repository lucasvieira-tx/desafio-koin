import csv 

from pathlib import Path
from typing import List, Dict, Any, Iterator

def read_csv(path: Path) -> Iterator[dict[str, str]]:
    """
    Read a CSV file and yield rows as dictionaries.
    
    Args:
        path: Path to the CSV file to read.
        
    Yields:
        Dictionary representing each row in the CSV file.
    """
    with open(path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            yield row

def write_csv(path: Path, data: List[Dict[str, Any]], fieldnames: List[str]) -> None:
    """
    Write data to a CSV file, overwriting if it exists.
    
    Args:
        path: Path to the CSV file to write.
        data: List of dictionaries representing rows to write.
        fieldnames: List of column names for the CSV file.
    """
    with open(path, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in data:
            writer.writerow(row)

def append_csv(path: Path, data: List[Dict[str, Any]], fieldnames: List[str]) -> None:
    """
    Append data to a CSV file, creating it if it doesn't exist.
    
    Args:
        path: Path to the CSV file to append to.
        data: List of dictionaries representing rows to append.
        fieldnames: List of column names for the CSV file.
    """
    file_exists = path.exists()
    with open(path, 'a', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        if not file_exists:
            writer.writeheader()
        for row in data:
            writer.writerow(row)