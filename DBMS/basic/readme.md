# 🔰 SQL Basics & Fundamental Queries

This directory focuses on foundational relational database operations in PostgreSQL, covering standard **DDL (Data Definition Language)**, **DML (Data Manipulation Language)**, and **DQL (Data Query Language)** including projection, filtering, sorting, and pattern matching.

---

## 📂 File Directory & Overview

| File Name | Topic | Key Concepts | Description |
| :--- | :--- | :--- | :--- |
| [`basic.sql`](./basic.sql) | Table Creation & Basic Filtering | `PRIMARY KEY`, `DEFAULT NULL`, `WHERE`, `AND` | Creates an `employee` table, inserts employee details, and executes basic conditional selection queries. |
| [`level.sql`](./level.sql) | Intermediate Filtering & Sorting | `BETWEEN`, `IN`, `LIKE`, `ORDER BY`, `LIMIT`, `DISTINCT` | Creates a `student` table and runs comprehensive query clauses including range filters, lists, regex-like matching, and pagination. |

---

## 🔍 Detailed File Breakdown

### 1. `basic.sql` (Employee Schema & Simple DQL)
- **Objective:** Practice table creation with default constraints and simple column projection & filtering.
- **Table Schema:**
  - `employee (id INT PRIMARY KEY, name VARCHAR(100), age INT, department VARCHAR(50), salary INT)`
- **Core Operations:**
  - Column projection: `SELECT name, salary FROM employee;`
  - Numeric comparison: `SELECT * FROM employee WHERE age >= 24;`
  - Multi-attribute conditions: `SELECT * FROM employee WHERE department = 'IT' AND salary >= 30000;`

---

### 2. `level.sql` (Student Schema & Analytical Clauses)
- **Objective:** Master PostgreSQL query clauses for data filtering, sorting, pattern matching, and aggregation preparation.
- **Table Schema:**
  - `student (id INT PRIMARY KEY, name VARCHAR(50), department VARCHAR(20), age INT, cgpa DECIMAL(3,2), city VARCHAR(50))`
- **Key Clauses Practiced:**
  - **Range Comparison:** `WHERE age BETWEEN 21 AND 24;`
  - **Membership Testing:** `WHERE city IN ('Dhaka', 'Rangpur');`
  - **Pattern Matching:** `WHERE name LIKE '%A%';` (case-sensitive substring matching)
  - **Sorting:** `ORDER BY cgpa DESC;` and `ORDER BY age ASC;`
  - **Pagination (Top-N):** `ORDER BY cgpa DESC LIMIT 3;`
  - **Deduplication:** `SELECT DISTINCT city FROM student;`
  - **Complex Boolean Logic:** 
    ```sql
    SELECT * FROM student 
    WHERE department IN ('CSE','EEE') 
      AND age BETWEEN 21 AND 24 
      AND cgpa >= 3.10;
    ```

---

## 🚀 Execution Guide

### Direct Execution via Terminal (`psql`)

```bash
# Execute basic employee script
psql -U postgres -d postgres -f DBMS/basic/basic.sql

# Execute student query practice script
psql -U postgres -d postgres -f DBMS/basic/level.sql
```

### Interactive Execution inside `psql` Shell

```sql
psql -U postgres -d postgres

\i DBMS/basic/basic.sql
\i DBMS/basic/level.sql
```

