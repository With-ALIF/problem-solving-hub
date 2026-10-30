DO $$ BEGIN
    INSERT INTO Department (DeptID, DeptName)
    VALUES (1, 'Civil Engineering');
EXCEPTION WHEN OTHERS THEN
    RAISE NOTICE 'EXPECTED FAILURE: %', SQLERRM;
END $$;

DO $$ BEGIN
    INSERT INTO Course (CourseID, Title, Credits, DeptID)
    VALUES ('CSE-301', 'Compiler Design', 5.0, 1);
EXCEPTION WHEN OTHERS THEN
    RAISE NOTICE 'EXPECTED FAILURE: %', SQLERRM;
END $$;

DO $$ BEGIN
    INSERT INTO Student (StudentID, Name, Email, DeptID, Profile)
    VALUES (201, 'Jamil Hossain', 'jamil@univ.edu', 999, '{"year": 1}'::jsonb);
EXCEPTION WHEN OTHERS THEN
    RAISE NOTICE 'EXPECTED FAILURE: %', SQLERRM;
END $$;

DO $$ BEGIN
    INSERT INTO Student (StudentID, Name, Email, DeptID, Profile)
    VALUES (202, 'Kamal Hossain', 'arif.hasan@example.com', 1, '{"year": 1}'::jsonb);
EXCEPTION WHEN OTHERS THEN
    RAISE NOTICE 'EXPECTED FAILURE: %', SQLERRM;
END $$;

DO $$ BEGIN
    INSERT INTO Course (CourseID, Title, Credits, DeptID)
    VALUES ('CSE-302', NULL, 3.0, 1);
EXCEPTION WHEN OTHERS THEN
    RAISE NOTICE 'EXPECTED FAILURE: %', SQLERRM;
END $$;

DO $$ BEGIN
    INSERT INTO Enrollment (StudentID, CourseID, Semester, Grade)
    VALUES (103, 'CSE-201', 'Fall 2024', NULL);
EXCEPTION WHEN OTHERS THEN
    RAISE NOTICE 'EXPECTED FAILURE: %', SQLERRM;
END $$;

DO $$ BEGIN
    INSERT INTO Student (StudentID, Name, Email, DeptID, Profile)
    VALUES (203, 'Rafiq Duplicate Check', 'RAFIQ@univ.edu', 1, '{"year": 2}'::jsonb);
EXCEPTION WHEN OTHERS THEN
    RAISE NOTICE 'EXPECTED FAILURE: %', SQLERRM;
END $$;

DELETE FROM Enrollment WHERE StudentID = 103 AND CourseID = 'CSE-201' AND Semester = 'Fall 2024';
DELETE FROM Student WHERE StudentID IN (201, 202, 203);

SELECT StudentID, Name FROM Student ORDER BY StudentID LIMIT 10;
