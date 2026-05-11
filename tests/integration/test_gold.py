from src.layers.gold import GoldProcessor
from src.schemas.customers import GoldCustomer
from src.schemas.orders import GoldOrder
from src.utils.csv_io import read_csv


def test_gold_process_customers():
    silver_path = "tests/data/silver/customersSilver.csv"
    gold_path = "tests/data/gold/customersGold.csv"
    rejected_path = "tests/data/rejected/customersGoldRejected.csv"

    gold = GoldProcessor()
    result = gold.process(
        silver_path,
        gold_path,
        rejected_path,
        GoldCustomer,
        field_transforms={
            "email": ("email_masked", gold._mask_email),
            "phone": ("phone_masked", gold._mask_phone),
            "name": ("name_masked", gold._mask_name),
        },
    )

    assert result == {
        "total_silver": 58,
        "valid": 58,
        "rejected_fk_violations": 0,
    }

    with open(gold_path, encoding="utf-8") as f:
        header = f.readline().strip().split(",")

    assert header == list(GoldCustomer.model_fields.keys())
    assert "email_masked" in header
    assert "phone_masked" in header
    assert "name_masked" in header
    assert "processed_at" in header

    assert "email" not in header
    assert "phone" not in header
    assert "name" not in header


def test_gold_process_orders_fk_constraint():
    silver_customers_path = "tests/data/silver/customersSilver.csv"
    silver_orders_path = "tests/data/silver/ordersSilver.csv"
    gold_path = "tests/data/gold/ordersGold.csv"
    rejected_path = "tests/data/rejected/ordersGoldRejected.csv"

    valid_customer_ids = {row["customer_id"] for row in read_csv(silver_customers_path)}

    result = GoldProcessor().process(
        silver_orders_path,
        gold_path,
        rejected_path,
        GoldOrder,
        valid_foreign_keys=valid_customer_ids,
        fk_field="customer_id",
    )

    assert result == {
        "total_silver": 122,
        "valid": 116,
        "rejected_fk_violations": 6,
    }

    with open(gold_path, encoding="utf-8") as f:
        header = f.readline().strip().split(",")

    assert header == list(GoldOrder.model_fields.keys())
    assert "processed_at" in header

    with open(rejected_path, encoding="utf-8") as f:
        rejected_rows = f.readlines()

    assert len(rejected_rows) == 7
