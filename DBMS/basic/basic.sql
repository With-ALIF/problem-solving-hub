CREATE TABLE employee (
    id INT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    age INT,
    department VARCHAR(50) DEFAULT NULL,
    salary INT DEFAULT NULL
);


INSERT INTO employee (id, name, age, department, salary)
VALUES
    (1, 'Alif', 22, 'IT', 300000),
    (2, 'Rahim', 25, 'HR', 28000),
    (3, 'Karim', 30, 'IT', 50000),
    (4, 'Sakib', 27, 'Finance', 40000),
    (5, 'Hasan', 21, 'IT', 25000);

SELECT * FROM employee;

SELECT name, salary FROM employee;

SELECT * FROM employee WHERE age >= 24;

SELECT * FROM employee WHERE department = 'IT' AND salary >= 30000;

