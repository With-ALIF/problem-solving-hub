# 📊 Result & Constraint Validation

This directory demonstrates schema integrity enforcement using PostgreSQL table-level constraints, specifically validation checks (`CHECK`) on academic grading schemes and grade point scales.

---

## 📂 File Directory & Overview

| File Name | Topic | Key Concepts | Description |
| :--- | :--- | :--- | :--- |
| [`result.sql`](./result.sql) | Data Integrity & Check Constraints | `CHECK`, `CONSTRAINT`, `IN`, `DECIMAL(3,2)`, `OR` | Implements a university student grading table with constraints ensuring valid letter grades and grade point ranges. |

---

## 🔍 Detailed File Breakdown

### `result.sql` (Student Result Schema & Grading Validation)
- **Objective:** Prevent invalid or corrupt academic data from entering the database by enforcing strict domain constraints directly at the schema level.
- **Table Schema:**
  ```sql
  CREATE TABLE Result (
      Student_id INT NOT NULL,
      Name VARCHAR(20) NOT NULL,
      Dept_Name VARCHAR(10) NOT NULL,
      GRADE VARCHAR(5),
      CONSTRAINT check_grade CHECK (
          GRADE IN ('A+', 'A', 'A-', 'B+', 'B', 'C', 'D', 'F')
      ),
      POINT DECIMAL(3,2) CHECK (
          POINT = 0 OR POINT BETWEEN 2 AND 4
      )
  );
  ```
- **Constraint Rules Enforced:**
  1. **Grade Set Membership:** The `check_grade` constraint restricts `GRADE` strictly to valid letter grades (`A+`, `A`, `A-`, `B+`, `B`, `C`, `D`, `F`). Any other string causes PostgreSQL to reject the insert.
  2. **Point Boundary & Zero Check:** The `POINT` constraint ensures GPA points fall within a realistic range (`POINT = 0` for failing grades, or `2.00` to `4.00` for passing grades).
- **Sample Records:**
  - Includes sample records across CSE, EEE, and BBA departments covering honors grades (`4.00`, `3.75`), average grades, and failing grades (`0.00`).

---

## 🚀 Execution Guide

### Direct Execution via Terminal (`psql`)

```bash
# Execute result script
psql -U postgres -d postgres -f DBMS/result/result.sql
```

### Interactive Execution inside `psql` Shell

```sql
psql -U postgres -d postgres

\i DBMS/result/result.sql
```

