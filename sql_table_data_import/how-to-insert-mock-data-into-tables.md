# Steps for inserting mock data in to tables


## 1) Download mock data from below website
https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce/discussion?sort=hotness

## 2) Create table schema
Create database in Postgres Server

```sql
-- =====================================================
-- 1. CUSTOMERS
-- =====================================================
CREATE TABLE customers (
    customer_id VARCHAR(50) PRIMARY KEY,
    customer_unique_id VARCHAR(50) NOT NULL,
    customer_zip_code_prefix INTEGER,
    customer_city VARCHAR(100),
    customer_state CHAR(2)
);

CREATE INDEX idx_customers_unique_id
ON customers(customer_unique_id);


-- =====================================================
-- 2. GEOLOCATION
-- =====================================================
CREATE TABLE geolocations (
    geolocation_zip_code_prefix INTEGER,
    geolocation_lat NUMERIC(10,8),
    geolocation_lng NUMERIC(11,8),
    geolocation_city VARCHAR(100),
    geolocation_state CHAR(2)
);

CREATE INDEX idx_geolocation_zip
ON geolocations(geolocation_zip_code_prefix);


-- =====================================================
-- 3. SELLERS
-- =====================================================
CREATE TABLE sellers (
    seller_id VARCHAR(50) PRIMARY KEY,
    seller_zip_code_prefix INTEGER,
    seller_city VARCHAR(100),
    seller_state CHAR(2)
);

CREATE INDEX idx_seller_zip
ON sellers(seller_zip_code_prefix);


-- =====================================================
-- 4. PRODUCT CATEGORY TRANSLATION
-- =====================================================
CREATE TABLE product_category_translations (
    product_category_name VARCHAR(100) PRIMARY KEY,
    product_category_name_english VARCHAR(100)
);


-- =====================================================
-- 5. PRODUCTS
-- =====================================================
CREATE TABLE products (
    product_id VARCHAR(50) PRIMARY KEY,

    product_category_name VARCHAR(100),

    product_name_length INTEGER,
    product_description_length INTEGER,
    product_photos_qty INTEGER,

    product_weight_g NUMERIC(10,2),
    product_length_cm NUMERIC(10,2),
    product_height_cm NUMERIC(10,2),
    product_width_cm NUMERIC(10,2),

    CONSTRAINT fk_product_category
    FOREIGN KEY (product_category_name)
    REFERENCES product_category_translations(product_category_name)
);

CREATE INDEX idx_product_category
ON products(product_category_name);


-- =====================================================
-- 6. ORDERS
-- =====================================================
CREATE TABLE orders (
    order_id VARCHAR(50) PRIMARY KEY,

    customer_id VARCHAR(50) NOT NULL,

    order_status VARCHAR(30),

    order_purchase_timestamp TIMESTAMP,
    order_approved_at TIMESTAMP,
    order_delivered_carrier_date TIMESTAMP,
    order_delivered_customer_date TIMESTAMP,
    order_estimated_delivery_date TIMESTAMP,

    CONSTRAINT fk_order_customer
    FOREIGN KEY (customer_id)
    REFERENCES customers(customer_id)
);

CREATE INDEX idx_orders_customer
ON orders(customer_id);

CREATE INDEX idx_orders_purchase_date
ON orders(order_purchase_timestamp);


-- =====================================================
-- 7. ORDER ITEMS
-- =====================================================
CREATE TABLE order_items (
    order_id VARCHAR(50),
    order_item_id INTEGER,

    product_id VARCHAR(50),
    seller_id VARCHAR(50),

    shipping_limit_date TIMESTAMP,

    price NUMERIC(12,2),
    freight_value NUMERIC(12,2),

    PRIMARY KEY (order_id, order_item_id),

    CONSTRAINT fk_item_order
        FOREIGN KEY (order_id)
        REFERENCES orders(order_id),

    CONSTRAINT fk_item_product
        FOREIGN KEY (product_id)
        REFERENCES products(product_id),

    CONSTRAINT fk_item_seller
        FOREIGN KEY (seller_id)
        REFERENCES sellers(seller_id)
);

CREATE INDEX idx_order_items_product
ON order_items(product_id);

CREATE INDEX idx_order_items_seller
ON order_items(seller_id);


-- =====================================================
-- 8. ORDER PAYMENTS
-- =====================================================
CREATE TABLE order_payments (
    order_id VARCHAR(50),
    payment_sequential INTEGER,

    payment_type VARCHAR(30),
    payment_installments INTEGER,
    payment_value NUMERIC(12,2),

    PRIMARY KEY(order_id, payment_sequential),

    CONSTRAINT fk_payment_order
    FOREIGN KEY(order_id)
    REFERENCES orders(order_id)
);

CREATE INDEX idx_payment_type
ON order_payments(payment_type);


-- =====================================================
-- 9. ORDER REVIEWS
-- =====================================================
CREATE TABLE order_reviews (
    review_id VARCHAR(50) PRIMARY KEY,

    order_id VARCHAR(50),

    review_score INTEGER,
    review_comment_title TEXT,
    review_comment_message TEXT,

    review_creation_date TIMESTAMP,
    review_answer_timestamp TIMESTAMP,

    CONSTRAINT fk_review_order
    FOREIGN KEY(order_id)
    REFERENCES orders(order_id)
);

CREATE INDEX idx_review_order
ON order_reviews(order_id);

CREATE INDEX idx_review_score
ON order_reviews(review_score);


CREATE INDEX idx_order_status
ON orders(order_status);

CREATE INDEX idx_customer_city
ON customers(customer_city);

CREATE INDEX idx_customer_state
ON customers(customer_state);

CREATE INDEX idx_seller_state
ON sellers(seller_state);

CREATE INDEX idx_order_delivered_date
ON orders(order_delivered_customer_date);

CREATE INDEX idx_review_creation_date
ON order_reviews(review_creation_date);

```



## 3) Populate mock data into tables

```sql
-- 1. customers
COPY customers (
    customer_id,
    customer_unique_id,
    customer_zip_code_prefix,
    customer_city,
    customer_state
)
FROM '/data/olist_customers_dataset.csv'
DELIMITER ','
CSV HEADER;


-- 2. geolocations
COPY geolocations (
    geolocation_zip_code_prefix,
    geolocation_lat,
    geolocation_lng,
    geolocation_city,
    geolocation_state
)
FROM '/data/olist_geolocation_dataset.csv'
DELIMITER ','
CSV HEADER;


-- 3. sellers
COPY sellers (
    seller_id,
    seller_zip_code_prefix,
    seller_city,
    seller_state
)
FROM '/data/olist_sellers_dataset.csv'
DELIMITER ','
CSV HEADER;


-- 4. product category translations
COPY product_category_translations (
    product_category_name,
    product_category_name_english
)
FROM '/data/product_category_name_translation.csv'
DELIMITER ','
CSV HEADER;


-- 5. products
COPY products (
    product_id,
    product_category_name,
    product_name_length,
    product_description_length,
    product_photos_qty,
    product_weight_g,
    product_length_cm,
    product_height_cm,
    product_width_cm
)
FROM '/data/olist_products_dataset.csv'
DELIMITER ','
CSV HEADER;


-- 6. orders
COPY orders (
    order_id,
    customer_id,
    order_status,
    order_purchase_timestamp,
    order_approved_at,
    order_delivered_carrier_date,
    order_delivered_customer_date,
    order_estimated_delivery_date
)
FROM '/data/olist_orders_dataset.csv'
DELIMITER ','
CSV HEADER;


-- 7. order_items
COPY order_items (
    order_id,
    order_item_id,
    product_id,
    seller_id,
    shipping_limit_date,
    price,
    freight_value
)
FROM '/data/olist_order_items_dataset.csv'
DELIMITER ','
CSV HEADER;


-- 8. order_payments
COPY order_payments (
    order_id,
    payment_sequential,
    payment_type,
    payment_installments,
    payment_value
)
FROM '/data/olist_order_payments_dataset.csv'
DELIMITER ','
CSV HEADER;


-- 9. order_reviews
COPY order_reviews (
    review_id,
    order_id,
    review_score,
    review_comment_title,
    review_comment_message,
    review_creation_date,
    review_answer_timestamp
)
FROM '/data/olist_order_reviews_dataset.csv'
DELIMITER ','
CSV HEADER;

```