INSERT INTO Department (DeptID, DeptName) VALUES
(1, 'Computer Science and Engineering'),
(2, 'Electrical and Electronic Engineering'),
(3, 'Mathematics'),
(4, 'Physics');

INSERT INTO Student (StudentID, Name, Email, DeptID, Profile) VALUES
(101, 'Arif Hasan', 'arif.hasan@example.com', 1, '{"interests": ["Databases", "Distributed Systems"], "year": 2, "cgpa": 3.85}'::jsonb),
(102, 'Fatema Akter', 'fatema.akter@example.com', 1, '{"interests": ["Machine Learning", "NLP"], "year": 2, "cgpa": 3.92}'::jsonb),
(103, 'Tanvir Ahmed', 'tanvir.ahmed@example.com', 2, '{"interests": ["Embedded Systems", "Robotics"], "year": 3, "cgpa": 3.65}'::jsonb),
(104, 'Nusrat Jahan', 'nusrat.jahan@example.com', 3, '{"interests": ["Linear Algebra", "Applied Calculus"], "year": 1, "cgpa": 3.78}'::jsonb),
(105, 'Mehedi Hasan', 'mehedi.hasan@example.com', 4, '{"interests": ["Quantum Physics", "Astrophysics"], "year": 1, "cgpa": 3.50}'::jsonb),
(106, 'Mohammad Rafiq', 'rafiq@univ.edu', 1, '{"interests": ["Algorithms", "Data Structures"], "year": 2, "cgpa": 3.70}'::jsonb);

INSERT INTO Course (CourseID, Title, Credits, DeptID) VALUES
('CSE-101', 'Structured Programming Language', 3.0, 1),
('CSE-102', 'Structured Programming Lab', 1.5, 1),
('CSE-201', 'Database Management Systems', 3.0, 1),
('EEE-101', 'Basic Electrical Engineering', 3.0, 2),
('MAT-101', 'Differential and Integral Calculus', 4.0, 3),
('PHY-101', 'General Physics', 3.0, 4);

INSERT INTO Enrollment (StudentID, CourseID, Semester, Grade) VALUES
(101, 'CSE-101', 'Fall 2023', 'A'),
(101, 'CSE-102', 'Fall 2023', 'A-'),
(101, 'CSE-201', 'Spring 2024', 'B+'),
(102, 'CSE-101', 'Fall 2023', 'A'),
(102, 'CSE-201', 'Spring 2024', NULL),
(103, 'EEE-101', 'Fall 2023', 'B'),
(104, 'MAT-101', 'Fall 2023', 'A'),
(105, 'PHY-101', 'Fall 2023', 'C+'),
(101, 'CSE-101', 'Spring 2024', 'A');

SELECT StudentID, Name FROM Student ORDER BY StudentID LIMIT 5;
SELECT CourseID, Title FROM Course ORDER BY CourseID LIMIT 5;
SELECT StudentID, CourseID, Semester, Grade FROM Enrollment ORDER BY StudentID LIMIT 5;
