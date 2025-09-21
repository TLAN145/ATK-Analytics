-- Customers
CREATE TABLE customers (
    customer_id VARCHAR PRIMARY KEY,
    customer_unique_id VARCHAR NOT NULL,
    customer_zip_code_prefix INT NOT NULL,
    customer_city VARCHAR,
    customer_state VARCHAR(2)
);

-- Orders
CREATE TABLE orders (
    order_id VARCHAR PRIMARY KEY,
    customer_id VARCHAR NOT NULL REFERENCES customers(customer_id),
    order_status VARCHAR,
    order_purchase_timestamp TIMESTAMP,
    order_approved_at TIMESTAMP,
    order_delivered_carrier_date TIMESTAMP,
    order_delivered_customer_date TIMESTAMP,
    order_estimated_delivery_date TIMESTAMP
);

-- Products
CREATE TABLE products (
    product_id VARCHAR PRIMARY KEY,
    product_category_name VARCHAR,
    product_name_lenght INT,
    product_description_lenght INT,
    product_photos_qty INT,
    product_weight_g INT,
    product_length_cm INT,
    product_height_cm INT,
    product_width_cm INT
);

-- Sellers
CREATE TABLE sellers (
    seller_id VARCHAR PRIMARY KEY,
    seller_zip_code_prefix INT NOT NULL,
    seller_city VARCHAR,
    seller_state VARCHAR(2)
);

-- Order Items
CREATE TABLE order_items (
    order_id VARCHAR NOT NULL REFERENCES orders(order_id),
    order_item_id INT NOT NULL,
    product_id VARCHAR NOT NULL REFERENCES products(product_id),
    seller_id VARCHAR NOT NULL REFERENCES sellers(seller_id),
    shipping_limit_date TIMESTAMP,
    price NUMERIC(10,2),
    freight_value NUMERIC(10,2),
    PRIMARY KEY (order_id, order_item_id)
);

-- Order Payments
CREATE TABLE order_payments (
    order_id VARCHAR NOT NULL REFERENCES orders(order_id),
    payment_sequential INT NOT NULL,
    payment_type VARCHAR,
    payment_installments INT,
    payment_value NUMERIC(10,2),
    PRIMARY KEY (order_id, payment_sequential)
);

-- Order Reviews
CREATE TABLE order_reviews (
    review_id VARCHAR PRIMARY KEY,
    order_id VARCHAR NOT NULL REFERENCES orders(order_id),
    review_score INT,
    review_comment_title TEXT,
    review_comment_message TEXT,
    review_creation_date TIMESTAMP,
    review_answer_timestamp TIMESTAMP
);

-- Geolocation
CREATE TABLE geolocation (
    geolocation_zip_code_prefix INT,
    geolocation_lat NUMERIC(9,6),
    geolocation_lng NUMERIC(9,6),
    geolocation_city VARCHAR,
    geolocation_state VARCHAR(2)
    -- no strict PK because many rows share same zip
);

-- Product Category Translation
CREATE TABLE product_category_name_translation (
    product_category_name VARCHAR PRIMARY KEY,
    product_category_name_english VARCHAR
);
