
USE customer360;

-- 1. Monthly revenue and orders
SELECT
    DATE_FORMAT(InvoiceDate, '%Y-%m') AS sales_month,
    ROUND(SUM(Revenue), 2) AS total_revenue,
    COUNT(DISTINCT InvoiceNo) AS total_orders
FROM sales_transactions
GROUP BY DATE_FORMAT(InvoiceDate, '%Y-%m')
ORDER BY sales_month;

-- 2. Top 10 customers by spending
SELECT
    CustomerID,
    ROUND(SUM(Revenue), 2) AS total_spending,
    COUNT(DISTINCT InvoiceNo) AS total_orders
FROM sales_transactions
WHERE CustomerID IS NOT NULL
GROUP BY CustomerID
ORDER BY total_spending DESC
LIMIT 10;

-- 3. Customer segment analysis
SELECT
    Segment,
    COUNT(*) AS customer_count,
    ROUND(AVG(Monetary), 2) AS average_spending,
    ROUND(AVG(Frequency), 2) AS average_orders
FROM customer_rfm
GROUP BY Segment
ORDER BY customer_count DESC;

-- 4. Top 10 products by revenue
SELECT
    StockCode,
    MAX(Description) AS product_name,
    ROUND(SUM(Revenue), 2) AS total_revenue,
    SUM(Quantity) AS units_sold
FROM sales_transactions
GROUP BY StockCode
ORDER BY total_revenue DESC
LIMIT 10;

-- 5. One-time vs repeat customers
SELECT
    CASE
        WHEN order_count = 1 THEN 'One-time customer'
        ELSE 'Repeat customer'
    END AS customer_type,
    COUNT(*) AS customer_count
FROM (
    SELECT
        CustomerID,
        COUNT(DISTINCT InvoiceNo) AS order_count
    FROM sales_transactions
    WHERE CustomerID IS NOT NULL
    GROUP BY CustomerID
) AS customer_orders
GROUP BY customer_type;
