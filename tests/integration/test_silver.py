from src.layers.silver import SilverProcessor
from src.schemas.customers import SilverCustomer
from src.schemas.orders import SilverOrder


def test_silver_process_customers_keep_first_reject_conflicting():
    bronze_path = "tests/data/bronze/customersBronze.csv"
    silver_path = "tests/data/silver/customersSilver.csv"
    rejected_path = "tests/data/rejected/customersRejected.csv"
    

    result = SilverProcessor().process(
        bronze_path,
        silver_path,
        rejected_path,
        SilverCustomer,
        "customer_id",
        ["customer_id", "cpf_hash", "name", "city", "state", "created_at", "status"],
        "keep_first_reject_conflicting",
    )

    assert result == {
        "total_bronze": 64,
        "valid": 58,
        "rejected": 6,
        "deduped": 4,
    }

    with open(silver_path, "r", encoding="utf-8") as file:
        header = file.readline().strip().split(",")
        assert header == list(SilverCustomer.model_fields.keys())

    with open(rejected_path, "r", encoding="utf-8") as file:
        header = file.readline().strip().split(",")
        assert "rejection_layer" in header
        assert "rejection_reason" in header


def test_silver_process_orders_keep_last():
    bronze_path = "tests/data/bronze/ordersBronze.csv"
    silver_path = "tests/data/silver/ordersSilver.csv"
    rejected_path = "tests/data/rejected/ordersRejected.csv"

    result = SilverProcessor().process(
        bronze_path,
        silver_path,
        rejected_path,
        SilverOrder,
        "order_id",
        ["order_id", "customer_id", "order_date", "payment_method", "status"],
        "keep_last",
    )

    assert result == {
        "total_bronze": 184,
        "valid": 122,
        "rejected": 58,
        "deduped": 4,
    }

    with open(silver_path, "r", encoding="utf-8") as file:
        header = file.readline().strip().split(",")
        assert header == list(SilverOrder.model_fields.keys())

    with open(rejected_path, "r", encoding="utf-8") as file:
        rejected_rows = file.readlines()
        assert len(rejected_rows) == 59
