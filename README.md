# Customer360 — Customer Behavior Analytics

\<p align="center">
&#x20; \<strong>Turning Retail Transaction Data into Customer Insights\</strong>
\</p>

\<p align="center">
&#x20; \<img src="[https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white](https://img.shields.io/badge/Python-3776AB?style=for-the-badge\&logo=python\&logoColor=white)" alt="Python" />
&#x20; \<img src="[https://img.shields.io/badge/Pandas-150458?style=for-the-badge&logo=pandas&logoColor=white](https://img.shields.io/badge/Pandas-150458?style=for-the-badge\&logo=pandas\&logoColor=white)" alt="Pandas" />
&#x20; \<img src="[https://img.shields.io/badge/MySQL-4479A1?style=for-the-badge&logo=mysql&logoColor=white](https://img.shields.io/badge/MySQL-4479A1?style=for-the-badge\&logo=mysql\&logoColor=white)" alt="MySQL" />
&#x20; \<img src="[https://img.shields.io/badge/Jupyter-F37626?style=for-the-badge&logo=jupyter&logoColor=white](https://img.shields.io/badge/Jupyter-F37626?style=for-the-badge\&logo=jupyter\&logoColor=white)" alt="Jupyter" />
&#x20; \<img src="[https://img.shields.io/badge/Power_BI-Planned-F2C811?style=for-the-badge&logo=powerbi&logoColor=black](https://img.shields.io/badge/Power_BI-Planned-F2C811?style=for-the-badge\&logo=powerbi\&logoColor=black)" alt="Power BI planned" />
\</p>

## Overview

**Customer360** is a customer behavior analytics project that transforms retail transaction data into actionable business insights. It combines Python-based data cleaning, exploratory data analysis (EDA), customer segmentation, and SQL analytics to understand purchasing patterns and customer value.

The project uses the **Online Retail dataset** to explore sales performance, identify valuable customers, analyze product demand, and segment customers using the RFM (Recency, Frequency, Monetary) framework.

## Business Objectives

- Analyze revenue trends and retail purchasing behavior.
- Identify top customers based on spending and purchase activity.
- Segment customers using RFM analysis.
- Identify loyal, promising, and at-risk customer groups.
- Analyze product performance and customer purchasing frequency.
- Prepare structured datasets for SQL analysis and future business intelligence dashboards.

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

The raw dataset is excluded from this repository to keep the project lightweight. Download it from the official source before running the notebook.

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
| Power BI             | Planned interactive dashboard              |

## Project Workflow

1. **Data collection** — obtain the original retail dataset.
2. **Data cleaning** — inspect missing values, remove duplicates, convert dates, and prepare transaction records.
3. **Feature engineering** — calculate transaction revenue and prepare analysis-ready data.
4. **Exploratory analysis** — investigate sales and customer purchasing patterns.
5. **RFM segmentation** — calculate customer recency, frequency, and monetary value and assign customer segments.
6. **Database integration** — load processed transaction and customer datasets into MySQL.
7. **SQL analytics** — query revenue trends, customer value, product performance, and repeat purchases.
8. **Visualization** — develop a Power BI dashboard as a planned project enhancement.

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

## Repository Structure

```text
Customer360/
│
├── data/
│   ├── raw/                  # Downloaded source data (not tracked)
│   └── processed/            # Generated CSV files (not tracked)
│
├── notebooks/
│   └── 01_exploratory_analysis.ipynb
│
├── sql/
│   └── customer_analysis.sql
│
├── src/
│   ├── data_cleaning.py
│   └── load_to_mysql.py
│
├── reports/                  # Future analysis outputs
├── dashboard/                # Planned Power BI dashboard
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

### 4. Download the dataset

Download the Online Retail Excel file from the [official UCI dataset page](https://archive.ics.uci.edu/dataset/352/online+retail).

Place the downloaded file at:

```text
data/raw/Online Retail.xlsx
```

### 5. Run the notebook

```bash
jupyter notebook
```

Open `notebooks/01_exploratory_analysis.ipynb` and run the cells in order.

The notebook generates processed transaction and customer RFM datasets in `data/processed/`.

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

Execute the queries in `sql/customer_analysis.sql` using MySQL Workbench or another MySQL client after the tables have been created.

## Current Project Status

- [x] Dataset exploration and cleaning
- [x] Revenue feature engineering
- [x] Customer RFM calculation and segmentation
- [x] Export processed datasets
- [x] Load processed data into MySQL
- [ ] Complete and validate the SQL analysis script
- [ ] Build an interactive Power BI dashboard
- [ ] Add dashboard screenshots and business findings
- [ ] Add further automated data-quality checks

## Future Enhancements

- Develop an interactive Power BI dashboard with KPI cards and trend analysis.
- Add customer retention and cohort analysis.
- Explore customer lifetime value estimation.
- Build product-level performance dashboards.
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
