INSERT INTO Student (StudentID, Name, Email, DeptID, Profile)
VALUES (
    1001,
    'Alice Rahaman',
    'alice.rahaman@univ.edu',
    1,
    '{
        "emergency_contact": {
            "name": "Farhana Rahaman",
            "relationship": "Mother",
            "phone": "+8801700000000"
        },
        "interests": ["AI", "Cybersecurity"]
    }'::jsonb
)
ON CONFLICT (StudentID) DO UPDATE 
SET Profile = EXCLUDED.Profile,
    Name    = EXCLUDED.Name,
    Email   = EXCLUDED.Email,
    DeptID  = EXCLUDED.DeptID;

SELECT 
    StudentID,
    Name,
    Profile -> 'emergency_contact' ->> 'phone' AS EmergencyPhone
FROM Student
WHERE StudentID = 1001;

SELECT 
    StudentID,
    Name, 
    Email,
    Profile -> 'interests' AS Interests
FROM Student
WHERE Profile @> '{"interests": ["AI"]}'
ORDER BY StudentID
LIMIT 5;

INSERT INTO Student (StudentID, Name, Email, DeptID, Profile)
SELECT 
    i AS StudentID,
    'Synthetic Student ' || i AS Name,
    'synthetic.student.' || i || '@univ.edu' AS Email,
    ((i % 4) + 1) AS DeptID,
    jsonb_build_object(
        'emergency_contact', jsonb_build_object(
            'name', 'Guardian ' || i,
            'relationship', CASE WHEN i % 2 = 0 THEN 'Father' ELSE 'Mother' END,
            'phone', '+88017' || LPAD(i::text, 8, '0')
        ),
        'interests', CASE 
            WHEN i % 50 = 0 THEN jsonb_build_array('AI', 'Robotics')
            WHEN i % 50 = 1 THEN jsonb_build_array('AI', 'Cybersecurity')
            ELSE jsonb_build_array('Networks', 'Web Development')
        END,
        'cgpa', ROUND((2.50 + (i % 150) * 0.01)::numeric, 2)
    ) AS Profile
FROM generate_series(10000, 109999) AS g(i)
ON CONFLICT (StudentID) DO NOTHING;

DROP INDEX IF EXISTS idx_student_profile_path_ops;
DROP INDEX IF EXISTS idx_student_profile;
ANALYZE Student;

EXPLAIN (ANALYZE, BUFFERS)
SELECT StudentID, Name
FROM Student
WHERE Profile @> '{"interests": ["AI"]}'
LIMIT 5;

CREATE INDEX idx_student_profile_path_ops 
ON Student USING GIN (Profile jsonb_path_ops);

ANALYZE Student;

EXPLAIN (ANALYZE, BUFFERS)
SELECT StudentID, Name
FROM Student
WHERE Profile @> '{"interests": ["AI"]}'
LIMIT 5;

SELECT 
    StudentID,
    Name,
    JSON_VALUE(Profile, '$.emergency_contact.name')         AS ContactName,
    JSON_VALUE(Profile, '$.emergency_contact.relationship') AS Relationship,
    JSON_VALUE(Profile, '$.emergency_contact.phone')        AS ContactPhone
FROM Student
WHERE StudentID = 1001;

SELECT 
    s.StudentID,
    s.Name,
    jt.Interest
FROM Student s,
JSON_TABLE(
    s.Profile,
    '$.interests[*]'
    COLUMNS (
        Interest VARCHAR(50) PATH '$'
    )
) AS jt
WHERE s.StudentID = 1001;

SELECT 
    s.StudentID,
    s.Name,
    jt.ContactName,
    jt.Relationship,
    jt.ContactPhone,
    jt.Interest
FROM Student s,
JSON_TABLE(
    s.Profile,
    '$'
    COLUMNS (
        ContactName  VARCHAR(100) PATH '$.emergency_contact.name',
        Relationship VARCHAR(50)  PATH '$.emergency_contact.relationship',
        ContactPhone VARCHAR(30)  PATH '$.emergency_contact.phone',
        NESTED PATH '$.interests[*]' COLUMNS (
            Interest VARCHAR(50) PATH '$'
        )
    )
) AS jt
WHERE s.StudentID = 1001;

ALTER TABLE Student DROP CONSTRAINT IF EXISTS chk_profile_interests;

ALTER TABLE Student
ADD CONSTRAINT chk_profile_interests
CHECK (
    Profile IS NULL
    OR NOT (Profile ? 'interests')
    OR jsonb_typeof(Profile -> 'interests') = 'array'
);

UPDATE Student
SET Profile = '{"interests": "AI"}'::jsonb
WHERE StudentID = 1001;
