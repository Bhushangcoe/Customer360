"""Clean Online Retail transactions and export sales and customer RFM data."""

from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
import pandas as pd


PROJECT_DIR = Path(__file__).resolve().parents[1]
DEFAULT_INPUT = PROJECT_DIR / "data" / "raw" / "Online Retail.xlsx"
DEFAULT_OUTPUT_DIR = PROJECT_DIR / "data" / "processed"

REQUIRED_COLUMNS = {
    "InvoiceNo",
    "StockCode",
    "Description",
    "Quantity",
    "InvoiceDate",
    "UnitPrice",
    "CustomerID",
    "Country",
}


def clean_transactions(raw_df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Return cleaned source rows and valid, completed sales transactions."""
    missing_columns = REQUIRED_COLUMNS.difference(raw_df.columns)
    if missing_columns:
        missing = ", ".join(sorted(missing_columns))
        raise ValueError(f"Source data is missing required columns: {missing}")

    clean_df = raw_df.drop_duplicates().copy()
    clean_df["InvoiceDate"] = pd.to_datetime(
        clean_df["InvoiceDate"], errors="coerce"
    )
    clean_df["CustomerID"] = clean_df["CustomerID"].astype("Int64")
    clean_df = clean_df.dropna(
        subset=["InvoiceNo", "StockCode", "InvoiceDate", "Quantity", "UnitPrice"]
    ).copy()
    clean_df["Revenue"] = clean_df["Quantity"] * clean_df["UnitPrice"]
    clean_df["IsCancelled"] = clean_df["InvoiceNo"].astype(str).str.startswith("C")

    sales_df = clean_df.loc[
        (~clean_df["IsCancelled"])
        & (clean_df["Quantity"] > 0)
        & (clean_df["UnitPrice"] > 0)
    ].copy()
    return clean_df, sales_df


def build_customer_rfm(sales_df: pd.DataFrame) -> pd.DataFrame:
    """Calculate RFM scores and rule-based segments for identified customers."""
    customer_sales = sales_df.dropna(subset=["CustomerID"])
    if customer_sales.empty:
        raise ValueError("No sales transactions have an identified CustomerID.")

    reference_date = sales_df["InvoiceDate"].max() + pd.Timedelta(days=1)
    rfm = (
        customer_sales.groupby("CustomerID")
        .agg(
            Recency=(
                "InvoiceDate",
                lambda dates: (reference_date - dates.max()).days,
            ),
            Frequency=("InvoiceNo", "nunique"),
            Monetary=("Revenue", "sum"),
        )
        .reset_index()
    )

    rfm["R_Score"] = pd.qcut(
        rfm["Recency"].rank(method="first"),
        5,
        labels=[5, 4, 3, 2, 1],
    ).astype(int)
    rfm["F_Score"] = pd.qcut(
        rfm["Frequency"].rank(method="first"),
        5,
        labels=[1, 2, 3, 4, 5],
    ).astype(int)
    rfm["M_Score"] = pd.qcut(
        rfm["Monetary"].rank(method="first"),
        5,
        labels=[1, 2, 3, 4, 5],
    ).astype(int)
    rfm["RFM_Score"] = (
        rfm["R_Score"].astype(str)
        + rfm["F_Score"].astype(str)
        + rfm["M_Score"].astype(str)
    )
    rfm["Segment"] = np.select(
        [
            (rfm["R_Score"] >= 4)
            & (rfm["F_Score"] >= 4)
            & (rfm["M_Score"] >= 4),
            (rfm["R_Score"] >= 3) & (rfm["F_Score"] >= 3),
            (rfm["R_Score"] <= 2) & (rfm["F_Score"] >= 3),
            (rfm["R_Score"] >= 4) & (rfm["F_Score"] <= 2),
        ],
        [
            "Champions",
            "Loyal Customers",
            "At Risk",
            "New or Promising",
        ],
        default="Needs Attention",
    )
    return rfm


def build_segment_summary(rfm: pd.DataFrame) -> pd.DataFrame:
    """Summarize customer counts and RFM metrics by segment."""
    return (
        rfm.groupby("Segment")
        .agg(
            Customers=("CustomerID", "nunique"),
            Average_Spend=("Monetary", "mean"),
            Total_Revenue=("Monetary", "sum"),
            Average_Orders=("Frequency", "mean"),
            Average_Recency_Days=("Recency", "mean"),
        )
        .round(2)
        .sort_values("Total_Revenue", ascending=False)
        .reset_index()
    )


def process_file(input_path: Path, output_dir: Path) -> None:
    """Clean the source workbook and write the three processed CSV files."""
    if not input_path.is_file():
        raise FileNotFoundError(f"Source workbook not found: {input_path}")

    raw_df = pd.read_excel(input_path)
    clean_df, sales_df = clean_transactions(raw_df)
    rfm = build_customer_rfm(sales_df)
    segment_summary = build_segment_summary(rfm)

    output_dir.mkdir(parents=True, exist_ok=True)
    sales_df.to_csv(output_dir / "sales_transactions.csv", index=False)
    rfm.to_csv(output_dir / "customer_rfm.csv", index=False)
    segment_summary.to_csv(output_dir / "segment_summary.csv", index=False)

    print(f"Original rows: {len(raw_df):,}")
    print(f"Cleaned rows: {len(clean_df):,}")
    print(f"Cancellation records: {int(clean_df['IsCancelled'].sum()):,}")
    print(f"Valid sales rows: {len(sales_df):,}")
    print(f"Identified customers: {len(rfm):,}")
    print(f"Revenue: {sales_df['Revenue'].sum():,.2f}")
    print(f"Processed files saved to: {output_dir.resolve()}")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Clean Online Retail data and create sales and RFM CSV files."
    )
    parser.add_argument(
        "--input",
        type=Path,
        default=DEFAULT_INPUT,
        help=f"Source Excel workbook (default: {DEFAULT_INPUT})",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=DEFAULT_OUTPUT_DIR,
        help=f"Directory for processed CSV files (default: {DEFAULT_OUTPUT_DIR})",
    )
    args = parser.parse_args()
    process_file(args.input, args.output_dir)


if __name__ == "__main__":
    main()