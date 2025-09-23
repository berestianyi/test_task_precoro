import argparse
import json
from decimal import Decimal

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.test_task.application import settings
from src.test_task.persistence.repository.product import ProductRepository


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-f", "--file",
        default="tools/fixtures/products.json",
    )
    args = parser.parse_args()

    engine = create_engine(settings.DATABASE_DSN, pool_pre_ping=True, future=True)
    SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False,
                                expire_on_commit=False, future=True)

    with open(args.file, "r", encoding="utf-8") as f:
        data = json.load(f)

    with SessionLocal.begin() as session:
        repo = ProductRepository(session)
        for row in data:
            repo.save(
                name=row["name"],
                price=Decimal(str(row["price"])),
                quantity=int(row["quantity"]),
            )

if __name__ == "__main__":
    main()
