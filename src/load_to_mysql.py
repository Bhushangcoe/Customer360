
from pathlib import Path
from getpass import getpass

import pandas as pd
from sqlalchemy import URL, create_engine, text

PROJECT_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = PROJECT_DIR / "data" / "processed"

sales_file = DATA_DIR / "sales_transactions.csv"
rfm_file = DATA_DIR / "customer_rfm.csv"

for file in [sales_file, rfm_file]:
    if not file.exists():
        raise FileNotFoundError(f"File not found: {file}")

username = input("MySQL username [root]: ").strip() or "root"
password = getpass("MySQL password: ")

url = URL.create(
    "mysql+pymysql",
    username=username,
    password=password,
    host="localhost",
    port=3306,
    database="customer360"
)

engine = create_engine(url)

try:
    with engine.connect() as connection:
        db_name = connection.execute(
            text("SELECT DATABASE()")
        ).scalar_one()
        print("Connected to database:", db_name)

    # Load customer RFM data
    rfm_df = pd.read_csv(rfm_file)
    rfm_df["CustomerID"] = pd.to_numeric(
        rfm_df["CustomerID"], errors="raise"
    ).astype("int64")

    rfm_df.to_sql(
        "customer_rfm",
        con=engine,
        if_exists="replace",
        index=False,
        chunksize=1000
    )
    print(f"Customer RFM rows imported: {len(rfm_df):,}")

    # Load sales transactions
    sales_df = pd.read_csv(
        sales_file,
        parse_dates=["InvoiceDate"]
    )
    sales_df["CustomerID"] = pd.to_numeric(
        sales_df["CustomerID"], errors="coerce"
    ).astype("Int64")

    sales_df.to_sql(
        "sales_transactions",
        con=engine,
        if_exists="replace",
        index=False,
        chunksize=1000
    )
    print(f"Sales transaction rows imported: {len(sales_df):,}")

    print("Customer360 import completed successfully!")

finally:
    engine.dispose()
