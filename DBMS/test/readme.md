# 🧪 Test & Practice Scripts

This directory contains introductory and experimental PostgreSQL scripts used for testing database setup, schema constraints, conflict handling, and PL/pgSQL procedural functions.

---

## 📂 File Directory & Overview

| File Name | Category | Description | Key Concepts |
| :--- | :--- | :--- | :--- |
| [`alif.sql`](./alif.sql) | DDL / DML | Creates a `student` table, inserts sample records, and handles duplicate names. | `SERIAL`, `PRIMARY KEY`, `UNIQUE`, `ON CONFLICT DO NOTHING` |
| [`sum.sql`](./sum.sql) | PL/pgSQL | Creates a user-defined function to calculate the sum of 3 integers with interactive CLI input. | `CREATE FUNCTION`, `plpgsql`, `\prompt`, Variable substitution |
| [`test.sql`](./test.sql) | DDL / DML | Sanity check script creating a `student` table and inserting sample test data. | `DROP TABLE`, Table Constraints, Batch Insertion |

---

## 🔍 Detailed File Breakdown

### 1. `alif.sql`
- **Purpose:** Demonstrates basic table initialization, auto-incrementing primary keys, unique constraints, and idempotent insert handling.
- **Workflow:**
  1. Drops `student` table if it already exists to ensure a clean state.
  2. Creates table with `id SERIAL PRIMARY KEY` and unique `name VARCHAR(100)`.
  3. Inserts 5 student names (`Alif`, `Rakibul`, `Arafat`, `Sagor`, `Hadi`).
  4. Uses `ON CONFLICT (name) DO NOTHING` to prevent errors on duplicate values.
  5. Queries all rows using `SELECT * FROM student;`.

### 2. `sum.sql`
- **Purpose:** Implements procedural logic using PL/pgSQL and illustrates dynamic user interaction within the `psql` shell.
- **Workflow:**
  1. Defines `sum_of_three(a INT, b INT, c INT)` function returning an `INT`.
  2. Prompts the user via `\prompt` to input three numbers (`num1`, `num2`, `num3`).
  3. Executes the function with positional arguments and displays the result as `total_sum`.

### 3. `test.sql`
- **Purpose:** Quick database verification script to check environment connectivity, table creation, and query output.
- **Workflow:**
  1. Resets the `student` table schema.
  2. Defines the schema structure with constraints.
  3. Populates with an alternative set of test records (`Alif`, `Rahim`, `Karim`, `Sakib`, `Nadia`).
  4. Fetches and outputs all inserted records.

---

## 🚀 How to Run

Make sure PostgreSQL is running and you have access to `psql`.

### Option A: From Command Line / Terminal

Run any script directly using `psql`:

```bash
# Run alif.sql
psql -U postgres -d postgres -f DBMS/test/alif.sql

# Run sum.sql (will prompt for inputs in terminal)
psql -U postgres -d postgres -f DBMS/test/sum.sql

# Run test.sql
psql -U postgres -d postgres -f DBMS/test/test.sql
```

### Option B: From Inside `psql` Shell

Connect to the PostgreSQL interactive terminal and run using `\i`:

```sql
-- Connect to database
psql -U postgres -d postgres

-- Execute scripts inside psql
\i DBMS/test/alif.sql
\i DBMS/test/sum.sql
\i DBMS/test/test.sql
```

