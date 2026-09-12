DROP TABLE IF EXISTS student;

CREATE TABLE student (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) UNIQUE
);

INSERT INTO student (name) VALUES
('Alif'),
('Rakibul'),
('Arafat'),
('Sagor'),
('Hadi')
ON CONFLICT (name) DO NOTHING;

SELECT * FROM student;