import psycopg2
import pandas as pd

# Database connection settings
DB_CONFIG = {
    "dbname": "olist_project",
    "user": "postgres",        # your postgres username
    "password": "your_password",  # your postgres password
    "host": "localhost",import psycopg2
import pandas as pd
import os

# Database connection settings
DB_CONFIG = {
    "dbname": "olist_project",
    "user": "postgres",        # your postgres username
    "password": "1045",        # your postgres password
    "host": "localhost",
    "port": 5432
}

# Create output folder if it doesn't exist
OUTPUT_DIR = "outputs"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# 10 analytical queries
QUERIES = {
    "total_customers_by_state": """
        SELECT customer_state, COUNT(*) AS total_customers
        FROM customers
        GROUP BY customer_state
        ORDER BY total_customers DESC;
    """,
    "monthly_order_trend": """
        SELECT DATE_TRUNC('month', order_purchase_timestamp) AS month, COUNT(*) AS total_orders
        FROM orders
        GROUP BY month
        ORDER BY month;
    """,
    "top_10_product_categories": """
        SELECT p.product_category_name, SUM(oi.price) AS total_sales
        FROM order_items oi
        JOIN products p ON oi.product_id = p.product_id
        GROUP BY p.product_category_name
        ORDER BY total_sales DESC
        LIMIT 10;
    """,
    "top_10_sellers_by_revenue": """
        SELECT s.seller_id, SUM(oi.price) AS revenue
        FROM order_items oi
        JOIN sellers s ON oi.seller_id = s.seller_id
        GROUP BY s.seller_id
        ORDER BY revenue DESC
        LIMIT 10;
    """,
    "average_delivery_time_by_state": """
        SELECT c.customer_state,
               AVG(o.order_delivered_customer_date - o.order_purchase_timestamp) AS avg_delivery_days
        FROM orders o
        JOIN customers c ON o.customer_id = c.customer_id
        WHERE o.order_delivered_customer_date IS NOT NULL
        GROUP BY c.customer_state
        ORDER BY avg_delivery_days;
    """,
    "most_common_payment_type": """
        SELECT payment_type, COUNT(*) AS count
        FROM order_payments
        GROUP BY payment_type
        ORDER BY count DESC;
    """,
    "average_review_score_by_category": """
        SELECT p.product_category_name, AVG(r.review_score) AS avg_score
        FROM order_reviews r
        JOIN orders o ON r.order_id = o.order_id
        JOIN order_items oi ON o.order_id = oi.order_id
        JOIN products p ON oi.product_id = p.product_id
        GROUP BY p.product_category_name
        ORDER BY avg_score DESC;
    """,
    "highest_freight_value_items": """
        SELECT oi.order_id, oi.product_id, oi.freight_value
        FROM order_items oi
        ORDER BY oi.freight_value DESC
        LIMIT 10;
    """,
    "revenue_by_customer_state": """
        SELECT c.customer_state, SUM(oi.price) AS revenue
        FROM order_items oi
        JOIN orders o ON oi.order_id = o.order_id
        JOIN customers c ON o.customer_id = c.customer_id
        GROUP BY c.customer_state
        ORDER BY revenue DESC;
    """,
    "number_of_reviews_by_score": """
        SELECT review_score, COUNT(*) AS total_reviews
        FROM order_reviews
        GROUP BY review_score
        ORDER BY review_score;
    """
}

def run_queries():
    try:
        # Connect to PostgreSQL
        conn = psycopg2.connect(**DB_CONFIG)
        print("✅ Connected to database")

        # Run all queries
        for name, query in QUERIES.items():
            print(f"\n▶️ Running query: {name}")
            df = pd.read_sql(query, conn)
            print(df)

            # Save each result to CSV in outputs/
            filepath = os.path.join(OUTPUT_DIR, f"{name}.csv")
            df.to_csv(filepath, index=False)
            print(f"📁 Saved result to {filepath}")

        conn.close()
        print("\n✅ All queries executed successfully")

    except Exception as e:
        print("❌ Error:", e)

if __name__ == "__main__":
    run_queries()

    "port": 5432
}

# Example queries (from queries.sql)
QUERIES = {
    "total_customers": "SELECT customer_state, COUNT(*) AS total_customers FROM customers GROUP BY customer_state ORDER BY total_customers DESC LIMIT 5;",
    "monthly_orders": "SELECT DATE_TRUNC('month', order_purchase_timestamp) AS month, COUNT(*) FROM orders GROUP BY month ORDER BY month LIMIT 5;",
    "top_products": "SELECT p.product_category_name, SUM(oi.price) AS total_sales FROM order_items oi JOIN products p ON oi.product_id = p.product_id GROUP BY p.product_category_name ORDER BY total_sales DESC LIMIT 5;"
}

def run_queries():
    try:
        # Connect to PostgreSQL
        conn = psycopg2.connect(**DB_CONFIG)
        print("✅ Connected to database")

        # Run queries
        for name, query in QUERIES.items():
            print(f"\n▶️ Running query: {name}")
            df = pd.read_sql(query, conn)
            print(df)

        conn.close()
        print("\n✅ Done")

    except Exception as e:
        print("❌ Error:", e)

if __name__ == "__main__":
    run_queries()
