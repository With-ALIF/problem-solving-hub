-- 1. Create table structure
DROP TABLE IF EXISTS orders;

CREATE TABLE orders (
    order_id INT NOT NULL PRIMARY KEY,
    customer_name VARCHAR(100) NOT NULL,
    customer_email VARCHAR(255) NOT NULL,
    product_id BIGINT NOT NULL,
    product_name VARCHAR(255) NOT NULL,
    product_info JSONB NOT NULL
);

-- 2. Insert 3 sample records
INSERT INTO orders (order_id, customer_name, customer_email, product_id, product_name, product_info)
VALUES
    (1, 'Alif', 'alif@example.com', 101, 'Mechanical Keyboard', '{"brand": "Keychron", "color": "Black", "wireless": true, "price": 8500}'),
    (2, 'Rahim', 'rahim@example.com', 102, 'Wireless Mouse', '{"brand": "Logitech", "dpi": 16000, "wireless": true, "price": 3200}'),
    (3, 'Karim', 'karim@example.com', 103, 'Gaming Monitor', '{"brand": "Dell", "size": "27 inch", "refresh_rate": "165Hz", "price": 28000}');

-- 3. Retrieve all records
SELECT * FROM orders;
