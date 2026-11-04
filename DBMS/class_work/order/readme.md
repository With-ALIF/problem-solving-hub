# 🛒 Orders Schema & Semi-Structured Data (JSONB)

This directory demonstrates relational schema design combined with semi-structured document storage using PostgreSQL's native **`JSONB`** data type for flexible product attributes.

---

## 📂 File Directory & Overview

| File Name | Topic | Key Concepts | Description |
| :--- | :--- | :--- | :--- |
| [`order.sql`](./order.sql) | E-Commerce Orders & Semi-Structured Attributes | `PRIMARY KEY`, `INT`, `JSONB`, `DROP TABLE`, `INSERT`, `SELECT` | Creates an orders table storing customer info, product identifiers, and nested JSON metadata (brand, specifications, price). |

---

## 🔍 Detailed File Breakdown

### `order.sql` (Orders Management Schema & JSONB Integration)
- **Objective:** Model an e-commerce order entry system that stores structured customer and product metadata alongside flexible, semi-structured product properties (such as specifications and dynamic attributes) using binary JSON (`JSONB`).
- **Table Schema:**
  ```sql
  CREATE TABLE orders (
      order_id INT NOT NULL PRIMARY KEY,
      customer_name VARCHAR(100) NOT NULL,
      customer_email VARCHAR(255) NOT NULL,
      product_id BIGINT NOT NULL,
      product_name VARCHAR(255) NOT NULL,
      product_info JSONB NOT NULL
  );
  ```
- **Key Features & Data Types:**
  1. **`PRIMARY KEY` (`order_id`):** Enforces unique identification for every placed order.
  2. **`JSONB` (`product_info`):** Stores pre-parsed binary JSON data. Unlike standard `JSON`, `JSONB` eliminates white space, allows indexing on nested keys (using GIN indexes), and offers high-performance querying and filtering on internal document properties.
  3. **Naming Convention (`orders`):** Uses the plural noun `orders` to cleanly avoid syntax conflicts with the SQL reserved keyword `ORDER` (e.g., `ORDER BY`).
- **Sample Records Included:**
  - Mechanical Keyboard with specifications: `brand`, `color`, `wireless`, and `price`.
  - Wireless Mouse with specifications: `brand`, `dpi`, `wireless`, and `price`.
  - Gaming Monitor with specifications: `brand`, `size`, `refresh_rate`, and `price`.

---

## 🚀 Execution Guide

### Direct Execution via Terminal (`psql`)

```bash
# Execute script against your database (replace 'postgres' with your DB name)
psql -U postgres -d postgres -f DBMS/class_work/order/order.sql
```

### Interactive Execution inside `psql` Shell

```sql
-- Connect to database
psql -U postgres -d postgres

-- Run script using meta-command
\i DBMS/class_work/order/order.sql
```

