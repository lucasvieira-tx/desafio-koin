import pytest

from src.layers.bronze import BronzeProcessor
from src.schemas import customers, orders

def test_bronze_process_data_customers():
    source_path = "tests/data/raw/customers.csv"
    output_path = "tests/data/bronze/customersBronze.csv"
    schema = customers.BronzeCustomer 

    bronze = BronzeProcessor()
    result = bronze.process(source_path, output_path, schema)

    assert "total" in result
    assert "valid" in result
    assert "invalid" in result
    expected_total = 64  
    expected_valid = 64  
    expected_invalid = 0  

    assert result["total"] == expected_total  
    assert result["valid"] == expected_valid  
    assert result["invalid"] == expected_invalid  

    # Verifica se o arquivo de saída foi criado e contém as colunas de metadados
    with open(output_path, "r") as f:
        header = f.readline().strip().split(",")
        assert "ingestion_timestamp" in header
        assert "source_file" in header
        assert "row_number" in header
        assert "is_valid" in header
        assert "error_msg" in header

def test_bronze_process_data_orders():
    source_path = "tests/data/raw/orders.csv"
    output_path = "tests/data/bronze/ordersBronze.csv"
    schema = orders.BronzeOrder

    bronze = BronzeProcessor()
    result = bronze.process(source_path, output_path, schema)

    assert "total" in result
    assert "valid" in result
    assert "invalid" in result
    expected_total = 184
    expected_valid = 184
    expected_invalid = 0 

    assert result["total"] == expected_total  
    assert result["valid"] == expected_valid  
    assert result["invalid"] == expected_invalid  

    # Verifica se o arquivo de saída foi criado e contém as colunas de metadados
    with open(output_path, "r") as f:
        header = f.readline().strip().split(",")
        assert "ingestion_timestamp" in header
        assert "source_file" in header
        assert "row_number" in header
        assert "is_valid" in header
        assert "error_msg" in header