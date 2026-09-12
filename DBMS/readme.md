<div align="center">

# 🗄️ Solving SQL (PostgreSQL)

<p align="center">
  <b>A dedicated repository for PostgreSQL database practice, query optimization, and DBMS problem-solving.</b><br>
  Department of Computer Science & Engineering (CSE) • Begum Rokeya University, Rangpur (BRUR)<br>
  <b>Course:</b> Database Management System | <b>Course Code:</b> CSE 2203
</p>

[![Database](https://img.shields.io/badge/Database-PostgreSQL-316192?style=flat-square&logo=postgresql&logoColor=white)](https://www.postgresql.org/)
[![Course Code](https://img.shields.io/badge/Course-CSE_2203-blue?style=flat-square)](#)
[![Dialect](https://img.shields.io/badge/Language-PL%2FpgSQL-00758F?style=flat-square&logo=postgresql&logoColor=white)](https://www.postgresql.org/docs/)
[![Author](https://img.shields.io/badge/Author-With--ALIF-181717?style=flat-square&logo=github)](https://github.com/With-ALIF)
[![Maintenance](https://img.shields.io/badge/Maintained%3F-Active-success?style=flat-square)](#)

</div>

---

## 📌 Overview

Welcome to **Solving SQL**! This module serves as a personal learning journal and lab practice archive for the **Database Management System** course (**Course Code: CSE 2203**). It is designed to reinforce core relational database principles, master standard SQL and PL/pgSQL, and sharpen query optimization skills.

Every solution is organized into independent `.sql` files, making it easy to practice, test, and understand key database concepts step-by-step.

---

## 🎯 Curriculum & Focus Areas

- 🏗️ **DDL & Schema Architecture** — Table definitions, data types, constraints (`PRIMARY KEY`, `FOREIGN KEY`, `CHECK`, `UNIQUE`), and schema alter statements.
- 📝 **DML & Data Manipulation** — Insert, update, delete, upsert (`ON CONFLICT`), cascading modifications, and transaction control (`COMMIT`, `ROLLBACK`).
- 🔍 **DQL & Query Fundamentals** — Filtering (`WHERE`, `LIKE`, `IN`), sorting, grouping, aggregations, and subqueries.
- 🔗 **Joins & Relational Algebra** — Inner, Left, Right, Full Outer, Cross, and Self Joins.
- ⚡ **Advanced SQL & Optimization** — Subqueries, CTEs (`WITH`), Window Functions, Views, and Indexing.
- ⚙️ **PL/pgSQL & Procedural Logic** — Stored procedures, user-defined functions, variables, and conditional logic.
- 🧠 **Lab Tasks & Coursework** — Academic assignments, real-world database problem-solving, and query optimization.

---

## 💻 Execution Guide

Ensure you have [PostgreSQL](https://www.postgresql.org/download/) installed and that the PostgreSQL service is active.

### 1. Direct Execution via `psql`

Execute any `.sql` file directly from the terminal against a specific database:

```yaml
# Syntax
psql -U <username> -d <database_name> -f <filename>.sql

# Example
psql -U postgres -d postgres -f test.sql
```

### 2. Interactive `psql` Shell

Connect to the PostgreSQL interactive terminal and run scripts internally:

```yaml
# Connect to PostgreSQL shell
psql -U postgres -d postgres

# Inside psql shell, load and execute the script
\i test.sql
```

---

<div align="center">
  <sub>Department of Computer Science & Engineering • Begum Rokeya University, Rangpur (BRUR)</sub>
</div>

