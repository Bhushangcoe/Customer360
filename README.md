# Customer360 — Customer Behavior Analytics

## Overview

**Customer360** is a customer behavior analytics project that transforms retail transaction data into actionable business insights. It combines Python-based data cleaning, exploratory data analysis (EDA), customer segmentation, and SQL analytics to understand purchasing patterns and customer value.

The project uses the **Online Retail dataset** to explore sales performance, identify valuable customers, analyze product demand, and segment customers using the RFM (Recency, Frequency, Monetary) framework.

## Business Objectives

- Analyze revenue trends and retail purchasing behavior.
- Identify top customers based on spending and purchase activity.
- Segment customers using RFM analysis.
- Identify loyal, promising, and at-risk customer groups.
- Analyze product performance and customer purchasing frequency.
- Prepare structured datasets for SQL analysis and business reporting.

## Dataset

**Source:** UCI Machine Learning Repository — Online Retail

The dataset contains transactions from a UK-based online retail business.

**Dataset characteristics:**

- Original records: approximately 541,909 transactions.
- Time period: December 2010 – December 2011.
- Includes invoice details, products, quantities, prices, customer identifiers, and countries.

**Key columns**

| Column        | Description                       |
| ------------- | --------------------------------- |
| `InvoiceNo`   | Invoice or transaction identifier |
| `StockCode`   | Product identifier                |
| `Description` | Product description               |
| `Quantity`    | Number of items purchased         |
| `InvoiceDate` | Transaction date and time         |
| `UnitPrice`   | Price per item                    |
| `CustomerID`  | Customer identifier               |
| `Country`     | Customer's country                |

Dataset source: [UCI Online Retail Dataset](https://archive.ics.uci.edu/dataset/352/online+retail)

The source workbook and processed CSVs are included in this repository. The source data is available from the [official UCI dataset page](https://archive.ics.uci.edu/dataset/352/online+retail).

## Tech Stack

| Technology           | Purpose                                    |
| -------------------- | ------------------------------------------ |
| Python               | Data processing and analysis               |
| Pandas & NumPy       | Data cleaning and transformation           |
| Matplotlib & Seaborn | Data visualization                         |
| Jupyter Notebook     | Exploratory analysis                       |
| MySQL                | Relational storage and SQL analytics       |
| SQLAlchemy & PyMySQL | Python-to-MySQL integration                |
| Scikit-learn         | Available for future analytical extensions |

## Project Workflow

1. **Data collection** — obtain the original retail dataset.
2. **Data cleaning** — inspect missing values, remove duplicates, convert dates, and prepare transaction records.
3. **Feature engineering** — calculate transaction revenue and prepare analysis-ready data.
4. **Exploratory analysis** — investigate sales and customer purchasing patterns.
5. **RFM segmentation** — calculate customer recency, frequency, and monetary value and assign customer segments.
6. **Database integration** — load processed transaction and customer datasets into MySQL.
7. **SQL analytics** — query revenue trends, customer value, product performance, and repeat purchases.
8. **Business findings** — review the data-backed results and caveats in `reports/business_insights.md`.

## Customer Segmentation: RFM Analysis

RFM analysis evaluates customers using three dimensions:

- **Recency (R):** How recently a customer made a purchase.
- **Frequency (F):** How often a customer purchased.
- **Monetary (M):** How much a customer spent.

The project calculates RFM metrics and uses score-based rules to assign customer segments.

| Segment          | Business interpretation                                          |
| ---------------- | ---------------------------------------------------------------- |
| Champions        | Recent, frequent, and high-value customers                       |
| Loyal Customers  | Customers with recurring purchase activity                       |
| At Risk          | Previously frequent customers who have not purchased recently    |
| New or Promising | Recently active customers with relatively low purchase frequency |
| Needs Attention  | Customers who do not meet the other segment rules                |

These segments can help a business prioritize customer retention, loyalty programs, and targeted marketing campaigns.

## MySQL Analytics

The processed data is stored in the `customer360` database.

| Table                | Purpose                                 |
| -------------------- | --------------------------------------- |
| `sales_transactions` | Cleaned transaction-level data          |
| `customer_rfm`       | Customer-level RFM metrics and segments |

The SQL analysis covers:

- Monthly revenue trends.
- Top 10 customers by spending.
- Customer distribution by RFM segment.
- Best-performing products by revenue.
- One-time versus repeat customer analysis.

SQL scripts are maintained in the `sql/` directory.

The SQL analysis is covered by local regression tests that execute all five query bodies against the processed CSVs using SQLite. The test translates MySQL's `DATE_FORMAT` expression to SQLite's `strftime`; run the queries in MySQL Workbench as described below for a final check against your MySQL server.

## Verified Results

The processed data contains 524,878 transaction rows from 1 December 2010 through 9 December 2011, with £10,642,110.80 in revenue across 19,960 invoices. The customer RFM table contains 4,338 identified customers. Read [reports/business_insights.md](reports/business_insights.md) for segment, retention, country, and data-quality findings and their interpretation.

Run the local SQL regression checks from the repository root:

```bash
python -m unittest discover -s tests -v
```

## Repository Structure

```text
Customer360/
│
├── data/
│   ├── raw/                  # Source workbook
│   └── processed/            # Analysis-ready CSV files
│
├── notebooks/
│   └── 01_exploratory_analysis.ipynb
├── reports/
│   └── business_insights.md
│
├── sql/
│   └── customer_analysis.sql
│
├── src/
│   ├── data_cleaning.py
│   └── load_to_mysql.py
│
├── tests/
│   └── test_sql_analysis.py
├── .gitignore
├── requirements.txt
└── README.md
```

## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/Bhushangcoe/Customer360.git
cd Customer360
```

### 2. Create and activate a virtual environment

On Windows:

```bash
python -m venv .venv
.venv\Scripts\activate
```

### 3. Install dependencies

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Check the dataset

The source workbook and processed CSV files are included under `data/`. To reproduce the analysis from a fresh copy, download the Online Retail Excel file from the [official UCI dataset page](https://archive.ics.uci.edu/dataset/352/online+retail) and place it at:

`data/raw/Online Retail.xlsx`

### 5. Clean the data and run the notebook

From the repository root, run the standalone cleaning script to reproduce the processed data:

```bash
python src/data_cleaning.py
```

By default, the script reads `data/raw/Online Retail.xlsx`, removes duplicate and incomplete records, flags cancelled invoices, filters to completed sales with positive quantity and price, calculates revenue, and builds customer RFM scores and segments.

It creates or replaces these files in `data/processed/`:

- `sales_transactions.csv` — valid transaction-level sales with revenue and cancellation fields.
- `customer_rfm.csv` — recency, frequency, monetary value, scores, and customer segment.
- `segment_summary.csv` — customer counts and average and total metrics by segment.

To use a different input workbook or output directory, pass `--input` and `--output-dir`:

```bash
python src/data_cleaning.py --input "data/raw/Online Retail.xlsx" --output-dir "data/processed"
```

Running the script again replaces the three CSV files in the selected output directory. Ensure you have a backup if you need to preserve existing outputs.

To explore the analysis and visualizations, start Jupyter:

```bash
jupyter notebook
```

Open `notebooks/01_exploratory_analysis.ipynb` to explore and visualize the data.

The notebook contains the project analysis; the script provides a repeatable command-line path for generating its processed datasets.

### 6. Configure MySQL

Install and start MySQL Server, then create the database:

```sql
CREATE DATABASE customer360;
```

Configure the database connection in `src/load_to_mysql.py` using your local MySQL settings. Keep passwords and other credentials private; do not commit them to GitHub.

Run the data-loading script:

```bash
python src/load_to_mysql.py
```

Execute the queries in `sql/customer_analysis.sql` using MySQL Workbench or another MySQL client after the tables have been created. To run the local regression checks without a MySQL server, use `python -m unittest discover -s tests -v`.

## Current Project Status

- [x] Dataset exploration and cleaning
- [x] Revenue feature engineering
- [x] Customer RFM calculation and segmentation
- [x] Export processed datasets
- [x] Load processed data into MySQL
- [x] Validate all five SQL analyses against the processed datasets
- [x] Document data-backed business findings

## Future Enhancements

- Add customer retention and cohort analysis.
- Explore customer lifetime value estimation.
- Add product-level performance analysis.
- Automate the data preparation and database-loading workflow.
- Investigate predictive customer churn and purchase behavior models.

## Key Learning Outcomes

This project demonstrates practical experience with:

- Data cleaning and preprocessing using Python.
- Exploratory data analysis and visualization.
- Feature engineering for business metrics.
- RFM-based customer segmentation.
- SQL querying and relational database integration.
- Organizing a reproducible analytics project with Git and GitHub.

## Author

**Bhushan Gangurde**

Data Science Learner | Python | SQL | Data Analytics

- GitHub: [@Bhushangcoe](https://github.com/Bhushangcoe)
- Project Repository: [Customer360](https://github.com/Bhushangcoe/Customer360)

---

*Customer360 is a portfolio project built for learning and demonstrating customer analytics workflows. The findings depend on the source dataset and the assumptions used during data cleaning and segmentation.*
