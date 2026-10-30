DELETE FROM Enrollment WHERE StudentID = 2001 OR CourseID = '201';
DELETE FROM Student WHERE StudentID = 2001;
DELETE FROM Course WHERE CourseID = '201';
DELETE FROM Department WHERE DeptID = 10;

INSERT INTO Department (DeptID, DeptName)
VALUES (10, 'Electrical Engineering');

INSERT INTO Course (CourseID, Title, Credits, DeptID)
VALUES ('201', 'Circuit Analysis', 3.0, 10);

INSERT INTO Student (StudentID, Name, Email, DeptID, Profile)
VALUES (
    2001, 
    'Bob Smith', 
    'bob.smith@univ.edu', 
    10, 
    '{"interests": ["Circuits", "Electronics"], "year": 1}'::jsonb
);

INSERT INTO Enrollment (StudentID, CourseID, Semester, Grade)
VALUES (2001, '201', 'Spring 2026', 'A');

SELECT 
    d.DeptID, d.DeptName, 
    c.CourseID, c.Title, 
    s.StudentID, s.Name, s.DeptID AS StudentDeptID,
    e.Semester, e.Grade
FROM Department d
JOIN Course c ON d.DeptID = c.DeptID
JOIN Student s ON d.DeptID = s.DeptID
JOIN Enrollment e ON s.StudentID = e.StudentID AND c.CourseID = e.CourseID
WHERE d.DeptID = 10;

DELETE FROM Department WHERE DeptID = 10;

SELECT StudentID, Name, DeptID, Email
FROM Student 
WHERE StudentID = 2001;

BEGIN;

DELETE FROM Enrollment 
WHERE StudentID = 2001 AND CourseID = '201' AND Semester = 'Spring 2026';

DELETE FROM Course 
WHERE CourseID = '201';

DELETE FROM Department 
WHERE DeptID = 10;

SELECT StudentID, Name, DeptID, Email
FROM Student 
WHERE StudentID = 2001;

SELECT COUNT(*) AS DeptCount FROM Department WHERE DeptID = 10;
SELECT COUNT(*) AS CourseCount FROM Course WHERE CourseID = '201';

COMMIT;

DELETE FROM Enrollment WHERE StudentID = 2001 OR CourseID = '201';
DELETE FROM Student WHERE StudentID = 2001;
DELETE FROM Course WHERE CourseID = '201';
DELETE FROM Department WHERE DeptID = 10;

INSERT INTO Department (DeptID, DeptName) VALUES (10, 'Electrical Engineering');
INSERT INTO Course (CourseID, Title, Credits, DeptID) VALUES ('201', 'Circuit Analysis', 3.0, 10);
INSERT INTO Student (StudentID, Name, Email, DeptID, Profile)
VALUES (2001, 'Bob Smith', 'bob.smith@univ.edu', 10, '{"year": 1}'::jsonb);
INSERT INTO Enrollment (StudentID, CourseID, Semester, Grade) VALUES (2001, '201', 'Spring 2026', 'A');

ALTER TABLE Course DROP CONSTRAINT fk_course_department;

ALTER TABLE Course
ADD CONSTRAINT fk_course_department
    FOREIGN KEY (DeptID) REFERENCES Department (DeptID)
    ON UPDATE CASCADE
    ON DELETE CASCADE;

DELETE FROM Department WHERE DeptID = 10;

SELECT DeptID, DeptName FROM Department WHERE DeptID = 10;
SELECT CourseID, Title, DeptID FROM Course WHERE CourseID = '201';
SELECT StudentID, CourseID, Semester, Grade FROM Enrollment WHERE StudentID = 2001;
SELECT StudentID, Name, DeptID FROM Student WHERE StudentID = 2001;

ALTER TABLE Course DROP CONSTRAINT fk_course_department;

ALTER TABLE Course
ADD CONSTRAINT fk_course_department
    FOREIGN KEY (DeptID) REFERENCES Department (DeptID)
    ON UPDATE CASCADE
    ON DELETE RESTRICT;

ALTER TABLE Course DROP CONSTRAINT fk_course_department;
ALTER TABLE Course
ADD CONSTRAINT fk_course_department
    FOREIGN KEY (DeptID) REFERENCES Department (DeptID)
    ON UPDATE CASCADE
    ON DELETE CASCADE;

ALTER TABLE Enrollment DROP CONSTRAINT fk_enrollment_course;
ALTER TABLE Enrollment
ADD CONSTRAINT fk_enrollment_course
    FOREIGN KEY (CourseID) REFERENCES Course (CourseID)
    ON UPDATE CASCADE
    ON DELETE CASCADE;

DELETE FROM Department WHERE DeptID = 10;

SELECT COUNT(*) AS DeptCount FROM Department WHERE DeptID = 10;

SELECT COUNT(*) AS CourseCount FROM Course WHERE CourseID = '201';

SELECT * FROM Enrollment WHERE StudentID = 2001;

SELECT StudentID, Name, DeptID FROM Student WHERE StudentID = 2001;

DELETE FROM Student WHERE StudentID = 2001;

ALTER TABLE Course DROP CONSTRAINT fk_course_department;
ALTER TABLE Course
ADD CONSTRAINT fk_course_department
    FOREIGN KEY (DeptID) REFERENCES Department (DeptID)
    ON UPDATE CASCADE
    ON DELETE RESTRICT;

ALTER TABLE Enrollment DROP CONSTRAINT fk_enrollment_course;
ALTER TABLE Enrollment
ADD CONSTRAINT fk_enrollment_course
    FOREIGN KEY (CourseID) REFERENCES Course (CourseID)
    ON UPDATE CASCADE
    ON DELETE RESTRICT;
