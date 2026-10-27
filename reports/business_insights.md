# Customer360 Business Insights

## Scope and definitions

These findings are calculated from the checked-in processed CSV files. The transaction period is 1 December 2010 to 9 December 2011. The source data uses pounds sterling (£). Revenue is `Quantity × UnitPrice`; the processed transaction file has no cancellation rows or negative quantities. The period includes a partial December 2011.

`sales_transactions.csv` includes transactions with and without a customer ID. RFM analysis can only cover identified customers, so RFM monetary totals are not the same as all-transaction revenue.

## Headline results

- **£10,642,110.80 revenue** across **19,960 distinct invoices** and **524,878 transaction rows**.
- **4,338 identified customers** are represented in the customer RFM table.
- **£8,887,208.89** of revenue is associated with identified customers. The remaining **£1,754,901.91 (16.5%)** has no customer ID.
- The average revenue per distinct invoice is **£533.17**. This includes invoices without an identified customer and should not be confused with average customer spend.
- Of identified customers, **2,845 (65.6%)** made more than one distinct purchase invoice; **1,493 (34.4%)** made one.

## Customer segments

| Segment | Customers | Share of identified customers | Segment revenue | Share of identified revenue | Average recency |
| --- | ---: | ---: | ---: | ---: | ---: |
| Champions | 942 | 21.7% | £5,737,952.12 | 64.6% | 12.50 days |
| Loyal Customers | 1,000 | 23.1% | £1,500,694.33 | 16.9% | 33.32 days |
| At Risk | 661 | 15.2% | £823,912.44 | 9.3% | 150.64 days |
| Needs Attention | 1,425 | 32.9% | £682,410.56 | 7.7% | 176.24 days |
| New or Promising | 310 | 7.1% | £142,239.44 | 1.6% | 18.10 days |

### Actions to consider

1. Protect Champions and Loyal Customers with relevant loyalty or early-access offers; together they account for about **81.4%** of identified-customer revenue.
2. Test a targeted win-back campaign for At Risk customers, then compare their subsequent purchase rate and spend with a holdout group.
3. Use a low-cost second-purchase journey for New or Promising and Needs Attention customers. Track conversion to a second invoice rather than measuring campaign opens alone.
4. Improve customer-ID capture at checkout. Anonymous transactions represent **132,186 rows (25.2%)** and **16.5% of revenue**, limiting customer-level attribution.

## Sales and product patterns

- **November 2011** is the highest-revenue month at **£1,503,866.78**; **February 2011** is the lowest at **£522,545.56**. November's amount is a single-month peak, not proof of a recurring seasonal pattern.
- The United Kingdom contributes **£9,001,744.09 (84.6%)** of revenue. This concentration supports prioritizing the UK in the first dashboard view while retaining country filters for international comparisons.
- The highest-revenue stock code is **DOT (DOTCOM POSTAGE)** at **£206,248.77**. This is a postage/service code, not a physical product; retain it in the all-code ranking but distinguish it from merchandise when making product decisions.

## Validation and caveats

- The SQL analysis returned all expected result sets against the processed CSVs: 13 months, 10 top customers, five segments covering 4,338 customers, 10 top stock codes, and one-time/repeat counts covering all 4,338 identified customers.
- RFM monetary value reconciles exactly to transaction revenue for rows with a customer ID: **£8,887,208.89**.
- The SQL regression suite executes the queries in SQLite after translating the MySQL-specific `DATE_FORMAT` expression to `strftime`. A MySQL server was not available in the validation environment, so run the SQL file in MySQL Workbench after loading the tables to confirm against the target MySQL version.
- The source spans roughly one year, and December 2011 ends on the 9th. Avoid interpreting the monthly peak as a stable annual trend.
- RFM segments are rule-based descriptions of this dataset, not validated predictions of future behavior. Validate campaign recommendations with controlled tests.
