# Relational Foundations — Test Bank & Lab Challenges
## Part 3: Advanced Extension Challenges (C1–C5)
**Target Database Engine:** PostgreSQL 18.x

---

## 1. Project Overview & Architecture

This repository contains the laboratory implementation for **"Relational Foundations — Test Bank & Lab Challenges"**. It explores advanced relational database design, data integrity enforcement, temporal modeling, foreign key dependency graphs, modern converged JSONB document storage, and cutting-edge features native to PostgreSQL 18.


## 2. Setup & Execution Guide

### Prerequisites
- PostgreSQL 18.0 or later installed and running.
- Command-line tool `psql` accessible in your PATH.
- Superuser access (`postgres`) or a role with privileges to create databases, extensions, and tables.

### Quick Start (Terminal Commands)

Execute the scripts against the target database `test_bank`:

```bash
# 1. Create the database (if not already existing)
psql -U postgres -c "CREATE DATABASE test_bank;"

# 2. Execute scripts in dependency order
psql -U postgres -d test_bank -f 01_schema.sql
psql -U postgres -d test_bank -f 02_setup.sql
psql -U postgres -d test_bank -f 03_negative_testing.sql
psql -U postgres -d test_bank -f 04_jsonb_exercise.sql
psql -U postgres -d test_bank -f 05_cascading_execution.sql
psql -U postgres -d test_bank -f 06_advanced_extension_challenges.sql
```

---

## 3. Challenge-by-Challenge Breakdown & University Defense Guide

### Challenge C1 — Case-Insensitive Email Uniqueness

#### Theoretical Grounding & Concept
Under the ANSI SQL standard and standard B-Tree indexing, string equality comparisons depend on the active collation. Standard `UNIQUE (Email)` constraints perform byte-wise or collation-sensitive string checks where `'alice.rahaman@univ.edu'` and `'ALICE.RAHAMAN@UNIV.EDU'` are evaluated as distinct non-equal keys. However, RFC 5321 specifies that the domain part of an email address is strictly case-insensitive, and in modern SMTP practice, all mailbox providers treat addresses case-insensitively.

#### Implementation & Defense
1. **Flaw Demonstration**: We insert student 3001 with `'ALICE.RAHAMAN@UNIV.EDU'`. The engine accepts the row despite student 1001 already possessing `'alice.rahaman@univ.edu'`.
2. **Safe Sanitization**: We delete the test duplicate before indexing to prevent `CREATE INDEX` aborts.
3. **Unique Expression Index**:
   ```sql
   CREATE UNIQUE INDEX idx_student_email_lower ON Student (lower(Email));
   ```
   This builds a functional index that indexes the computed result of `lower(Email)` rather than the raw column value.
4. **Expected Rejection**:
   Attempting to insert `'Alice.Rahaman@Univ.Edu'` triggers:
   - **SQLSTATE**: `23505` (`unique_violation`)
   - **Constraint/Index**: `idx_student_email_lower`
5. **Key Defense Insight**: An expression index preserves the user's original casing preference in storage (e.g. for display purposes) while guaranteeing mailbox-level uniqueness at zero application-layer overhead.

---

### Challenge C2 — Temporal Primary Key for Department Heads

#### Theoretical Grounding & Concept
Traditional relational modeling struggles with historical time intervals. In university administration, a department may have multiple heads over its history, but **at any single instant in time, exactly one department head may preside**. Modeling this with scalar `start_date` and `end_date` columns requires complex, concurrency-vulnerable application triggers.

**PostgreSQL 18 Feature**: Native SQL:2011 temporal constraint support using `WITHOUT OVERLAPS`:
```sql
CONSTRAINT pk_depthead PRIMARY KEY (DeptID, ValidPeriod WITHOUT OVERLAPS)
```

#### Implementation & Defense
1. **Extension Requirement**:
   `CREATE EXTENSION IF NOT EXISTS btree_gist;`
   *Why?* The `WITHOUT OVERLAPS` clause builds a Generalized Search Tree (GiST) index. GiST natively supports 2D bounding box and range comparisons, but indexing a scalar integer (`DeptID`) alongside a range (`ValidPeriod`) requires the `btree_gist` operator class.
2. **Half-Open Intervals `[start, end)`**:
   - `[` indicates the start date is **inclusive**.
   - `)` indicates the end date is **exclusive**.
   - *Academic Justification*: If Dr. Turing's tenure is `[2020-01-01, 2022-01-01)` and Dr. Lovelace's tenure is `[2022-01-01, 2024-01-01)`, the changeover occurs at the exact midnight boundary of `2022-01-01`. Because `2022-01-01` is excluded from the first tenure, there is **zero overlapping second and zero missing day**.
3. **Expected Results**:
   - Consecutive tenures: Insert succeeds (`00000`).
   - Overlapping tenure (`[2021-06-01, 2023-01-01)`): Fails with **SQLSTATE `23P01`** (`exclusion_violation`).

---

### Challenge C3 — Circular Foreign Keys & Deferred Checking

#### Theoretical Grounding & Concept
When two tables reference each other circularly:
- `Instructor.DeptID -> Department.DeptID (NOT NULL)`
- `Department.ChairID -> Instructor.InstructorID`

Under default immediate constraint evaluation (`NOT DEFERRABLE`), it is impossible to insert either entity first without violating referential integrity. This classic relational dilemma is solved via transaction-level constraint deferral.

#### Implementation & Defense
1. **Constraint Configuration**:
   ```sql
   FOREIGN KEY (DeptID) REFERENCES Department(DeptID) DEFERRABLE INITIALLY DEFERRED;
   FOREIGN KEY (ChairID) REFERENCES Instructor(InstructorID) DEFERRABLE INITIALLY DEFERRED;
   ```
2. **Transaction Mechanics**:
   - `BEGIN;`
   - `INSERT INTO Department (DeptID, DeptName, ChairID) VALUES (20, 'Aerospace Engineering', 501);`
     *(Instructor 501 does not exist yet; check is queued).*
   - `INSERT INTO Instructor (InstructorID, Name, DeptID) VALUES (501, 'Dr. Neil Armstrong', 20);`
     *(Department 20 exists; check is queued).*
   - `COMMIT;`
     *(At commit time, PostgreSQL evaluates all queued deferred constraints simultaneously. Since both rows exist, the commit succeeds without error).*
3. **Key Defense Insight**: `DEFERRABLE INITIALLY DEFERRED` enables transient relational inconsistencies inside a single transaction while guaranteeing strict ACID consistency upon commit.

---

### Challenge C4 — Constraints on Legacy Data

#### Theoretical Grounding & Concept
Adding a constraint to a production table containing millions of rows presents two distinct enterprise engineering problems:
1. **Downtime**: Scanning a large table holds an exclusive table lock.
2. **Dirty Historical Data**: Existing non-compliant rows will cause the `ALTER TABLE` statement to fail immediately, preventing the enforcement of the rule on future transactions.

#### Implementation & Defense
#### Part A: `NOT VALID` and `VALIDATE CONSTRAINT`
- `ALTER TABLE StudentLegacy ADD CONSTRAINT chk_legacy_cgpa_range CHECK (CGPA BETWEEN 0.00 AND 4.00) NOT VALID;`
  - Takes a brief lock (`SHARE ROW EXCLUSIVE`).
  - **Does not scan existing rows**: instantly succeeds even though row 2 contains `CGPA = -1.50`.
  - Enforces the check immediately for all subsequent `INSERT` and `UPDATE` operations.
- `ALTER TABLE StudentLegacy VALIDATE CONSTRAINT chk_legacy_cgpa_range;`
  - When run before cleaning data: Fails with **SQLSTATE `23514`** (`check_violation`).
  - After updating the legacy dirty row: Succeeds with a light `SHARE UPDATE EXCLUSIVE` lock, scanning the table concurrently without blocking concurrent `SELECT`, `INSERT`, `UPDATE`, or `DELETE` statements.

#### Part B: PostgreSQL 18 `CHECK (...) NOT ENFORCED`
- `CONSTRAINT chk_priority_doc CHECK (Priority BETWEEN 1 AND 5) NOT ENFORCED`
  - Introduced in **PostgreSQL 18** to satisfy the SQL standard.
  - The constraint is recorded in `pg_constraint` with `conenforced = FALSE`.
  - **Does not reject violating rows** (e.g. inserting `Priority = 99` succeeds).
  - *Purpose*: Used for machine-readable schema documentation, metadata extraction by object-relational mappers (ORMs), and data warehouse ingestion pipelines where upstream ETL handles validation.

---

### Challenge C5 — Time-Ordered UUIDv7 Keys (PostgreSQL 18 Native)

#### Theoretical Grounding & Concept
When synthetic keys require global decentralization without an auto-incrementing central counter, developers historically reached for UUIDv4 (`gen_random_uuid()`). However, UUIDv4 is completely pseudo-random.

| Performance Characteristic | Random UUIDv4 (`gen_random_uuid()`) | Time-Ordered UUIDv7 (`uuidv7()`) |
| :--- | :--- | :--- |
| **B-Tree Insertion Locality** | Random across entire index tree | Appended to the rightmost leaf page |
| **Leaf Page Splits** | Very high (splits throughout the tree) | Extremely low (amortized linear growth) |
| **Buffer Cache Thrashing** | Severe (entire index must stay in RAM) | Minimal (only working rightmost edge cached) |
| **Chronological Ordering** | None | Natural chronological sort order |
| **Time Extraction** | Requires a separate `created_at` column | Native via `uuid_extract_timestamp(id)` |

#### PostgreSQL 18 Built-in Implementation
PostgreSQL 18 introduces native RFC 9562 UUIDv7 functions without requiring third-party extensions:
```sql
CREATE TABLE SecurityEventAudit (
    EventID UUID DEFAULT uuidv7() PRIMARY KEY,
    EventType VARCHAR(50) NOT NULL,
    ActorEmail VARCHAR(150) NOT NULL,
    RecordedAt TIMESTAMPTZ DEFAULT clock_timestamp()
);
```

#### Built-in PostgreSQL 18 Verification Functions
- `uuidv7()`: Generates a 128-bit UUID whose most significant 48 bits represent Unix epoch time in milliseconds.
- `uuid_extract_timestamp(EventID)`: Reconstructs the exact `timestamptz` timestamp encoded inside the UUID.
- `uuid_extract_version(EventID)`: Returns the integer value `7`.

#### Defense Discussion: Limitations & Trade-offs
1. **Timestamp Exposure / Security**: Because the creation time is encoded into the first 48 bits, UUIDv7 reveals the approximate generation timestamp. For public tokens (e.g. password reset links, secure session tokens), UUIDv4 or cryptographic random strings must still be used.
2. **Storage Footprint**: UUIDv7 consumes 16 bytes (128 bits), compared to 4 bytes for `INT` and 8 bytes for `BIGINT`. For tables where storage bandwidth is the primary bottleneck, `BIGINT IDENTITY` remains superior.

---

## 4. Expected SQLSTATE and Error Code Summary

| Challenge | Operation Tested | Expected Outcome | SQLSTATE Code | Error / Constraint Name |
| :--- | :--- | :--- | :--- | :--- |
| **C1** | Duplicate email differing only by case | **Blocked** | `23505` | `idx_student_email_lower` |
| **C2** | Overlapping department head tenure | **Blocked** | `23P01` | `pk_depthead` (`WITHOUT OVERLAPS`) |
| **C3** | Circular foreign key insertion | **Succeeds at COMMIT** | `00000` | `DEFERRABLE INITIALLY DEFERRED` |
| **C4-A** | Write invalid CGPA with `NOT VALID` active | **Blocked** | `23514` | `chk_legacy_cgpa_range` |
| **C4-A** | Validate dirty legacy data | **Blocked** | `23514` | `chk_legacy_cgpa_range` |
| **C4-A** | Validate sanitized legacy data | **Succeeds** | `00000` | `VALIDATE CONSTRAINT` |
| **C4-B** | Insert invalid value into `NOT ENFORCED` check | **Succeeds** | `00000` | Informational constraint |
| **C5** | Native `uuidv7()` generation & timestamp extraction | **Succeeds** | `00000` | Native PostgreSQL 18 RFC 9562 |
