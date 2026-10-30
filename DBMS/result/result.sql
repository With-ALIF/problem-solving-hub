DROP TABLE IF EXISTS Result;

CREATE TABLE Result (
    Student_id INT NOT NULL,
    Name VARCHAR(20) NOT NULL,
    Dept_Name VARCHAR(10) NOT NULL,

    GRADE VARCHAR(5),
    CONSTRAINT check_grade CHECK(
        GRADE IN('A+', 'A', 'A-', 'B+', 'B', 'C', 'D', 'F')
    ),

    POINT DECIMAL(3,2)
    CHECK (POINT = 0 OR POINT BETWEEN 2 AND 4)
);

INSERT INTO Result (Student_id, Name, Dept_Name, GRADE, Point)
VALUES
(1, 'Alif', 'CSE', 'A+', 4.00),
(2, 'Rahim', 'EEE', 'A', 3.75),
(3, 'Karim', 'CSE', 'B+', 3.50),
(4, 'Hasan', 'BBA', 'B', 3.00),
(5, 'Sakib', 'CSE', 'C', 2.50),
(6, 'Nila', 'EEE', 'F', 0);

SELECT * FROM Result;