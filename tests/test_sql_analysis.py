import re
import sqlite3
import unittest
from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]


class CustomerAnalysisSqlTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.connection = sqlite3.connect(":memory:")
        processed_dir = PROJECT_ROOT / "data" / "processed"

        for filename, table_name in (
            ("sales_transactions.csv", "sales_transactions"),
            ("customer_rfm.csv", "customer_rfm"),
        ):
            frame = pd.read_csv(processed_dir / filename, low_memory=False)
            frame.to_sql(
                table_name,
                cls.connection,
                index=False,
                if_exists="replace",
                chunksize=25_000,
            )

        sql = (PROJECT_ROOT / "sql" / "customer_analysis.sql").read_text(
            encoding="utf-8"
        )
        cls.queries = []
        for statement in sql.split(";"):
            statement = statement.strip()
            if not statement or re.match(r"USE\b", statement, flags=re.IGNORECASE):
                continue
            statement = re.sub(
                r"DATE_FORMAT\s*\(\s*InvoiceDate\s*,\s*'%Y-%m'\s*\)",
                "strftime('%Y-%m', InvoiceDate)",
                statement,
                flags=re.IGNORECASE,
            )
            cls.queries.append(statement)

    @classmethod
    def tearDownClass(cls):
        cls.connection.close()

    def run_query(self, query_number):
        return pd.read_sql_query(self.queries[query_number - 1], self.connection)

    def test_script_contains_five_analysis_queries(self):
        self.assertEqual(len(self.queries), 5)

    def test_monthly_revenue_covers_all_months_and_matches_sales(self):
        monthly = self.run_query(1)
        sales = pd.read_csv(
            PROJECT_ROOT / "data" / "processed" / "sales_transactions.csv",
            parse_dates=["InvoiceDate"],
            low_memory=False,
        )
        expected_revenue = (
            sales.assign(month=sales["InvoiceDate"].dt.to_period("M"))
            .groupby("month")["Revenue"]
            .sum()
            .round(2)
            .sum()
        )

        self.assertEqual(len(monthly), 13)
        self.assertAlmostEqual(monthly["total_revenue"].sum(), expected_revenue, 2)

    def test_top_customers_returns_ten_ranked_customers(self):
        top_customers = self.run_query(2)

        self.assertEqual(len(top_customers), 10)
        self.assertEqual(int(top_customers.iloc[0]["CustomerID"]), 14646)

    def test_segment_counts_cover_all_rfm_customers(self):
        segments = self.run_query(3)

        self.assertEqual(len(segments), 5)
        self.assertEqual(int(segments["customer_count"].sum()), 4338)

    def test_top_products_returns_ten_ranked_products(self):
        top_products = self.run_query(4)

        self.assertEqual(len(top_products), 10)
        self.assertEqual(top_products.iloc[0]["StockCode"], "DOT")

    def test_one_time_and_repeat_counts_cover_identified_customers(self):
        customer_types = self.run_query(5).set_index("customer_type")

        self.assertEqual(
            customer_types["customer_count"].to_dict(),
            {"One-time customer": 1493, "Repeat customer": 2845},
        )


if __name__ == "__main__":
    unittest.main()
