from pathlib import Path

from src.layers.bronze import BronzeProcessor
from src.layers.gold import GoldProcessor
from src.layers.silver import SilverProcessor
from src.schemas.customers import BronzeCustomer, GoldCustomer, SilverCustomer
from src.schemas.orders import BronzeOrder, GoldOrder, SilverOrder
from src.utils.csv_io import read_csv


def run_pipeline(data_dir: Path = Path("data")) -> None:
    raw_path = data_dir / "raw"
    bronze_path = data_dir / "bronze"
    silver_path = data_dir / "silver"
    gold_path = data_dir / "gold"
    rejected_path = data_dir / "rejected"

    for directory in [bronze_path, silver_path, gold_path, rejected_path]:
        directory.mkdir(parents=True, exist_ok=True)

    bronze = BronzeProcessor()
    silver = SilverProcessor()
    gold = GoldProcessor()

    # TODO: Implement the bronze layer
    bronze.process(
        raw_path / "customers.csv", bronze_path / "customersBronze.csv", BronzeCustomer
    )
    bronze.process(
        raw_path / "orders.csv", bronze_path / "ordersBronze.csv", BronzeOrder
    )

    # TODO: Implement the silver layer
    silver.process(
        bronze_path / "customersBronze.csv",
        silver_path / "customersSilver.csv",
        rejected_path / "customersRejected.csv",
        SilverCustomer,
        "customer_id",
        ["customer_id", "cpf_hash", "name", "city", "state", "created_at", "status"],
        "keep_first_reject_conflicting",
    )
    silver.process(
        bronze_path / "ordersBronze.csv",
        silver_path / "ordersSilver.csv",
        rejected_path / "ordersRejected.csv",
        SilverOrder,
        "order_id",
        ["order_id", "customer_id", "order_date", "payment_method", "status"],
        "keep_last",
    )

    # TODO: Implement the gold layer
    valid_customer_ids = {
        row["customer_id"] for row in read_csv(silver_path / "customersSilver.csv")
    }

    gold.process(
        silver_path / "customersSilver.csv",
        gold_path / "customersGold.csv",
        rejected_path / "customersGoldRejected.csv",
        GoldCustomer,
        field_transforms={
            "email": ("email_masked", gold._mask_email),
            "phone": ("phone_masked", gold._mask_phone),
            "name": ("name_masked", gold._mask_name),
        },
    )

    gold.process(
        silver_path / "ordersSilver.csv",
        gold_path / "ordersGold.csv",
        rejected_path / "ordersGoldRejected.csv",
        GoldOrder,
        valid_foreign_keys=valid_customer_ids,
        fk_field="customer_id",
    )


if __name__ == "__main__":
    run_pipeline()
