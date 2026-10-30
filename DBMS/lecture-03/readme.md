# 📚 Lecture 03: Modern Data Models in PostgreSQL

This directory explores advanced, multi-modal data modeling in PostgreSQL, combining **Relational Tables**, **Semi-Structured Document Storage (JSONB)**, **Geospatial Processing (PostGIS)**, and **Vector Similarity Search (pgvector)**.

---

## 📂 File Directory & Overview

| File Name | Topic | Key Technologies | Description |
| :--- | :--- | :--- | :--- |
| [`student.sql`](./student.sql) | Semi-Structured Data | `JSONB`, `GIN Index`, `@>` | Stores student profiles in JSONB format, builds a GIN index, and queries nested attributes with containment operators. |
| [`vector.sql`](./vector.sql) | AI & Vector Embeddings | `pgvector`, `HNSW Index`, `<=>` | Creates high-dimensional vector embeddings (`1536`-dim), indexes with HNSW, and performs cosine distance nearest-neighbor queries. |
| [`course.sql`](./course.sql) | Multi-Model Architecture | Relational + `JSONB` + `PostGIS` + `pgvector` | Unifies Relational, Document, Spatial, and Vector data into a single schema with hybrid geospatial & similarity search queries. |

---

## 🔍 Detailed File Breakdown

### 1. `student.sql` (JSONB & Document Modeling)
- **Objective:** Manage nested, schema-less document data natively inside PostgreSQL without sacrificing query performance.
- **Key Concepts:**
  - `JSONB` data type: Binary representation of JSON with indexability.
  - **GIN (Generalized Inverted Index):** Accelerates queries over keys and key-value pairs inside documents.
  - **Containment Operator (`@>`):** Checks whether the left JSONB document contains the right JSONB structure.
- **Query Highlights:**
  ```sql
  -- Search for student by nested emergency contact phone number
  SELECT * FROM student 
  WHERE profile @> '{"emergency_contact": {"phone": "01326571634"}}';
  ```

---

### 2. `vector.sql` (Semantic & Vector Similarity Search)
- **Objective:** Store and query text embedding vectors (e.g., OpenAI `text-embedding-3-small` / Ada-002 compatible 1536-dimensional vectors) for semantic search.
- **Key Concepts:**
  - `CREATE EXTENSION IF NOT EXISTS vector;` enables vector operations.
  - Column definition: `description_vector vector(1536)`.
  - Synthetic embedding generation via `generate_series(1, 1536)` and `array_agg(random())::vector`.
  - **HNSW (Hierarchical Navigable Small World) Index:** Fast approximate nearest neighbor (ANN) search.
  - **Cosine Distance Operator (`<=>`):** Computes cosine distance between vectors (1 - cosine similarity).
- **Query Highlights:**
  ```sql
  -- Find the top 3 most semantically similar courses to a query vector
  SELECT course_code, title
  FROM course
  ORDER BY description_vector <=> (:query_vector)
  LIMIT 3;
  ```

---

### 3. `course.sql` (One Table, Four Data Models)
- **Objective:** Demonstrates PostgreSQL as a unified multi-model database engine, avoiding polyglot persistence overhead.
- **Architectural Pillars:**
  1. **Relational:** `dept_id INT REFERENCES department(dept_id)` ensures relational integrity.
  2. **Document (JSONB):** `metadata JSONB` stores course attributes (e.g., level, credits, semester) indexed with GIN.
  3. **Geospatial (PostGIS):** `location GEOMETRY(Point, 4326)` stores coordinates indexed with GiST, enabling distance calculations via `ST_Distance` and `ST_DWithin`.
  4. **Vector (`pgvector`):** `description_embedding VECTOR(1536)` indexed with HNSW for semantic course matching.
- **Hybrid Query Example:**
  Filters by department (Relational), checks graduate level (JSONB), limits to a 2km radius (PostGIS), and ranks results by semantic cosine similarity (`pgvector`):
  ```sql
  SELECT c.course_code, c.title,
         ST_Distance(c.location::geography, ST_SetSRID(ST_MakePoint(89.2755, 25.7435), 4326)::geography) AS distance_m,
         c.description_embedding <=> array_fill(0.12::real, ARRAY[1536])::vector AS similarity
  FROM course c
  WHERE c.dept_id = 10
    AND c.metadata @> '{"level": "graduate"}'
    AND ST_DWithin(c.location::geography, ST_SetSRID(ST_MakePoint(89.2755, 25.7435), 4326)::geography, 2000)
  ORDER BY similarity
  LIMIT 5;
  ```

---

## ⚙️ Prerequisites & Setup

Before executing these scripts, ensure the required PostgreSQL extensions are installed on your server:

```sql
-- PostGIS (Geospatial support)
CREATE EXTENSION IF NOT EXISTS postgis;

-- pgvector (Vector embeddings support)
CREATE EXTENSION IF NOT EXISTS vector;
```

---

## 🚀 Execution Guide

### Direct Execution via Terminal (`psql`)

```bash
# Run student JSONB script
psql -U postgres -d postgres -f DBMS/lecture-03/student.sql

# Run vector search script
psql -U postgres -d postgres -f DBMS/lecture-03/vector.sql

# Run multi-model course script
psql -U postgres -d postgres -f DBMS/lecture-03/course.sql
```

### Interactive Execution inside `psql` Shell

```sql
psql -U postgres -d postgres

\i DBMS/lecture-03/student.sql
\i DBMS/lecture-03/vector.sql
\i DBMS/lecture-03/course.sql
```

