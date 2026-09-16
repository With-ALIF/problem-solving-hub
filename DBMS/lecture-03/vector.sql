DROP TABLE IF EXISTS course;

CREATE EXTENSION IF NOT EXISTS vector;

CREATE TABLE course (
    id SERIAL PRIMARY KEY,
    course_code VARCHAR(50) NOT NULL,
    title VARCHAR(200) NOT NULL,
    description TEXT,
    description_vector vector(1536)
);

INSERT INTO course (course_code, title, description) VALUES
('CSE1101', 'Introduction to Computer Science', 'This course introduces students to computer science and programming. '),
('CSE2201', 'Data Structures and Algorithms', 'This course introduces students to data structures and algorithms. '),
('CSE2203', 'Database Management Systems', 'This course introduces students to database management systems. '),
('CSE2205', 'Computer Architecture', 'This course covers computer architecture and organization. '),
('CSE2207', ' Operating System', 'This course covers operating system. '),
('CSE2209', 'Computer Networks', 'This course covers computer networks. ');

UPDATE course SET description_vector = (
    SELECT array_agg(random())::vector FROM generate_series(1, 1536)
) WHERE course_code = 'CSE1101';

UPDATE course SET description_vector = (
    SELECT array_agg(random())::vector FROM generate_series(1, 1536)
) WHERE course_code = 'CSE2201';

UPDATE course SET description_vector = (
    SELECT array_agg(random())::vector FROM generate_series(1, 1536)
) WHERE course_code = 'CSE2203';

UPDATE course SET description_vector = (
    SELECT array_agg(random())::vector FROM generate_series(1, 1536)
) WHERE course_code = 'CSE2205';

UPDATE course SET description_vector = (
    SELECT array_agg(random())::vector FROM generate_series(1, 1536)
) WHERE course_code = 'CSE2207';

UPDATE course SET description_vector = (
    SELECT array_agg(random())::vector FROM generate_series(1, 1536)
) WHERE course_code = 'CSE2209';


CREATE INDEX idx_course_vector
ON course USING hnsw(description_vector vector_cosine_ops);

SELECT course_code, title
FROM course
ORDER BY description_vector <=> (
    SELECT array_agg(random())::vector FROM generate_series(1, 1536)
)
LIMIT 3;
