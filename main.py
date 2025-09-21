import psycopg2
import pandas as pd

# Database connection settings
DB_CONFIG = {
    "dbname": "olist_project",
    "user": "postgres",        # your postgres username
    "password": "your_password",  # your postgres password
    "host": "localhost",
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
