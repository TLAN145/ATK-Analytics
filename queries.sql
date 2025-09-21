--- 4A
SELECT COUNT(*) FROM customers;
SELECT COUNT(*) FROM orders;
SELECT COUNT(*) FROM products;
SELECT COUNT(*) FROM sellers;
SELECT COUNT(*) FROM order_items;
SELECT COUNT(*) FROM order_payments;
SELECT COUNT(*) FROM order_reviews;
SELECT COUNT(*) FROM geolocation;
SELECT COUNT(*) FROM product_category_name_translation;

--- 4B
--1
SELECT * FROM orders LIMIT 10;
--2
SELECT *
FROM orders
WHERE order_status = 'delivered'
ORDER BY order_purchase_timestamp DESC
LIMIT 10;
--3
SELECT order_status, COUNT(*) AS total_orders
FROM orders
GROUP BY order_status;

SELECT AVG(payment_value) AS avg_payment,
       MIN(payment_value) AS min_payment,
       MAX(payment_value) AS max_payment
FROM order_payments;
--4
SELECT o.order_id, c.customer_city, c.customer_state, op.payment_value
FROM orders o
JOIN customers c ON o.customer_id = c.customer_id
JOIN order_payments op ON o.order_id = op.order_id
LIMIT 10;

--- 4C
--1
-- Count of customers per state
SELECT customer_state, COUNT(*) AS total_customers
FROM customers
GROUP BY customer_state
ORDER BY total_customers DESC;
--2
-- Number of orders per month
SELECT DATE_TRUNC('month', order_purchase_timestamp) AS month, COUNT(*) AS total_orders
FROM orders
GROUP BY month
ORDER BY month;
--3
-- Top product categories by total sales value
SELECT p.product_category_name, SUM(oi.price) AS total_sales
FROM order_items oi
JOIN products p ON oi.product_id = p.product_id
GROUP BY p.product_category_name
ORDER BY total_sales DESC
LIMIT 10;
--4
-- Sellers ranked by revenue
SELECT s.seller_id, SUM(oi.price) AS revenue
FROM order_items oi
JOIN sellers s ON oi.seller_id = s.seller_id
GROUP BY s.seller_id
ORDER BY revenue DESC
LIMIT 10;
--5
-- Avg delivery days per customer state
SELECT c.customer_state, AVG(o.order_delivered_customer_date - o.order_purchase_timestamp) AS avg_delivery_days
FROM orders o
JOIN customers c ON o.customer_id = c.customer_id
WHERE o.order_delivered_customer_date IS NOT NULL
GROUP BY c.customer_state
ORDER BY avg_delivery_days;
--6
-- Distribution of payment types
SELECT payment_type, COUNT(*) AS count
FROM order_payments
GROUP BY payment_type
ORDER BY count DESC;
--7
-- Average review score per category
SELECT p.product_category_name, AVG(r.review_score) AS avg_score
FROM order_reviews r
JOIN orders o ON r.order_id = o.order_id
JOIN order_items oi ON o.order_id = oi.order_id
JOIN products p ON oi.product_id = p.product_id
GROUP BY p.product_category_name
ORDER BY avg_score DESC;
--8
-- Top 10 order items by freight value
SELECT oi.order_id, oi.product_id, oi.freight_value
FROM order_items oi
ORDER BY oi.freight_value DESC
LIMIT 10;
--9
-- Total sales revenue by state
SELECT c.customer_state, SUM(oi.price) AS revenue
FROM order_items oi
JOIN orders o ON oi.order_id = o.order_id
JOIN customers c ON o.customer_id = c.customer_id
GROUP BY c.customer_state
ORDER BY revenue DESC;
--10
-- Count of reviews per score
SELECT review_score, COUNT(*) AS total_reviews
FROM order_reviews
GROUP BY review_score
ORDER BY review_score;
