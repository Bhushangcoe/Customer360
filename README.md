

\# Customer360 — Customer Behavior Analytics



\## Overview

Customer360 is an e-commerce analytics project that analyzes

customer purchasing behavior, sales performance, and customer

segments using Python, SQL, and RFM analysis.



\## Objectives

\- Analyze sales and revenue trends.

\- Identify top customers and products.

\- Segment customers using Recency, Frequency, and Monetary value.

\- Compare repeat and one-time customers.

\- Prepare data for an interactive Power BI dashboard.



\## Technology Stack

\- Python

\- Pandas and NumPy

\- Matplotlib and Seaborn

\- Jupyter Notebook

\- MySQL

\- SQL

\- Power BI (planned)



\## Dataset

The project uses the UCI Online Retail dataset.



The original dataset contains online retail transactions.

Raw data and processed CSV files are excluded from this repository.



\## Project Structure

```text

Customer360/

├── data/

│   ├── raw/

│   └── processed/

├── notebooks/

│   └── 01\_exploratory\_analysis.ipynb

├── sql/

│   └── customer\_analysis.sql

├── src/

│   ├── data\_cleaning.py

│   └── load\_to\_mysql.py

├── dashboard/

├── reports/

├── .gitignore

├── requirements.txt

└── README.md

```



\## Current Progress

\- Data cleaning and exploratory analysis.

\- Revenue and order analysis.

\- RFM customer segmentation.

\- CSV export.

\- MySQL database import.

\- SQL business analysis.



\## How to Run

1\. Clone this repository.

2\. Create and activate a Python virtual environment.

3\. Install dependencies using `pip install -r requirements.txt`.

4\. Download the Online Retail dataset and place it at

&#x20;  `data/raw/Online Retail.xlsx`.

5\. Run the Jupyter notebook in `notebooks/`.

6\. Configure a local MySQL database named `customer360`.

7\. Run `python src/load\_to\_mysql.py` to import the processed CSV files.



\## Note

This project is a learning and portfolio project.

Business findings should be interpreted in the context of the dataset.



