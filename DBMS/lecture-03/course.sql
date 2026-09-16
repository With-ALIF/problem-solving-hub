-- ============================================
-- ONE TABLE, FOUR DATA MODELS
-- PostgreSQL + JSONB + Spatial + Vector
-- ============================================

\set QUIET on

DROP TABLE IF EXISTS course;
DROP TABLE IF EXISTS department;

CREATE EXTENSION IF NOT EXISTS postgis;
CREATE EXTENSION IF NOT EXISTS vector;

\set QUIET off

CREATE TABLE department (
    dept_id SERIAL PRIMARY KEY,
    dept_name VARCHAR(100) NOT NULL
);

INSERT INTO department (dept_id, dept_name)
VALUES
    (10, 'Computer Science and Engineering'),
    (20, 'Electrical and Electronic Engineering'),
    (30, 'Mathematics');

CREATE TABLE course (
    course_id BIGSERIAL PRIMARY KEY,
    dept_id INT REFERENCES department(dept_id),
    course_code VARCHAR(20) NOT NULL,
    title VARCHAR(250) NOT NULL,
    metadata JSONB,
    location GEOMETRY(Point, 4326),
    description_embedding VECTOR(1536)
);

INSERT INTO course (
    dept_id,
    course_code,
    title,
    metadata,
    location,
    description_embedding
)
VALUES
(
    10,
    'CSE501',
    'Advanced Artificial Intelligence',
    '{"level": "graduate", "credits": 3, "semester": 1}',
    ST_SetSRID(ST_MakePoint(89.2750, 25.7439), 4326),
    array_fill(0.10::real, ARRAY[1536])::vector
),
(
    10,
    'CSE502',
    'Machine Learning',
    '{"level": "graduate", "credits": 3, "semester": 1}',
    ST_SetSRID(ST_MakePoint(89.2800, 25.7460), 4326),
    array_fill(0.20::real, ARRAY[1536])::vector
),
(
    10,
    'CSE503',
    'Database Systems',
    '{"level": "graduate", "credits": 3, "semester": 2}',
    ST_SetSRID(ST_MakePoint(89.2700, 25.7400), 4326),
    array_fill(0.30::real, ARRAY[1536])::vector
),
(
    10,
    'CSE504',
    'Computer Networks',
    '{"level": "undergraduate", "credits": 3, "semester": 2}',
    ST_SetSRID(ST_MakePoint(89.2760, 25.7420), 4326),
    array_fill(0.40::real, ARRAY[1536])::vector
),
(
    20,
    'EEE501',
    'Advanced Electronics',
    '{"level": "graduate", "credits": 3, "semester": 1}',
    ST_SetSRID(ST_MakePoint(89.2740, 25.7440), 4326),
    array_fill(0.50::real, ARRAY[1536])::vector
),
(
    10,
    'CSE505',
    'Deep Learning',
    '{"level": "graduate", "credits": 3, "semester": 2}',
    ST_SetSRID(ST_MakePoint(89.2780, 25.7445), 4326),
    array_fill(0.15::real, ARRAY[1536])::vector
);

CREATE INDEX idx_course_dept
ON course(dept_id);

CREATE INDEX idx_course_metadata
ON course USING GIN(metadata);

CREATE INDEX idx_course_location
ON course USING GIST(location);

CREATE INDEX idx_course_embedding
ON course USING HNSW (description_embedding vector_cosine_ops);

SELECT
    c.course_code,
    c.title,
    ST_Distance(
        c.location::geography,
        ST_SetSRID(
            ST_MakePoint(89.2755, 25.7435),
            4326
        )::geography
    ) AS distance_m,
    c.description_embedding <=>
        array_fill(0.12::real, ARRAY[1536])::vector
        AS similarity
FROM course c
WHERE c.dept_id = 10
AND c.metadata @> '{"level": "graduate"}'
AND ST_DWithin(
    c.location::geography,
    ST_SetSRID(
        ST_MakePoint(89.2755, 25.7435),
        4326
    )::geography,
    2000
)
ORDER BY
    c.description_embedding <=>
    array_fill(0.12::real, ARRAY[1536])::vector
LIMIT 5;