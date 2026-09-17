DROP TABLE IF EXISTS student;

CREATE TABLE student (
    id INT PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    department VARCHAR(20) NOT NULL,
    age INT NOT NULL,
    cgpa decimal(3,2) NOT NULL,
    city VARCHAR(50) NOT NULL
);


--- insert data

INSERT INTO student (id, name, department, age, cgpa, city)
VALUES
(1, 'ALIF', 'CSE', 22, 2.74, 'Rangpur'),
(2, 'RAHIM', 'EEE', 25, 3.25, 'Dhaka'),
(3, 'KARIM', 'CSE', 21, 3.50, 'Rangpur'),
(4, 'SAMI', 'EEE', 23, 3.20, 'Dhaka'),
(5, 'ANIKA', 'CSE', 22, 3.10, 'Rajshahi'),
(6, 'TOMA', 'BBA', 23, 2.90, 'Chittagong'),
(7, 'Sakib', 'BBA', 24, 3.10, 'Rajshahi'),
(8, 'Fahim', 'CSE', 22, 3.60, 'Chittagong'),
(9, 'Riya', 'EEE', 23, 2.80, 'Dhaka'),
(10, 'Akash', 'EEE', 21, 2.90, 'Rajshahi');


SELECT * FROM student;

SELECT * FROM student WHERE cgpa >= 3.50;

SELECT * FROM student  WHERE age BETWEEN 21 And 24;

SELECT * FROM student WHERE city IN ('Dhaka', 'Rangpur');

SELECT * FROM student WHERE name LIKE '%A%';

SELECT * FROM student ORDER BY cgpa DESC;

SELECT * FROM student ORDER BY age ASC;

SELECT * FROM student ORDER BY cgpa DESC LIMIT 3;

SELECT DISTINCT city FROM student;

SELECT * FROM student WHERE department IN ('CSE','EEE') AND age BETWEEN 21 AND 24 and cgpa >= 3.10;
