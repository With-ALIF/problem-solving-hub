/*
Create a student table in PostgreSQL with student_id, name, and profile (JSONB) columns.
 Insert data for three students,
 create a GIN index on the profile column,
 and use the @> operator to search for students whose emergency contact relationship is 
 guardian or self and search for a student by name.
*/

DROP TABLE IF EXISTS student;

CREATE TABLE student (
 student_id BIGINT PRIMARY KEY,
 name VARCHAR(100) NOT NULL,
 profile JSONB
);


CREATE INDEX student_profile_idx
ON student USING GIN (profile);


INSERT INTO student (student_id , name , profile) VALUES 
   (
    101,
    'ALIF',
    '{
        "emergency_contact": {
            "name": "Kalid",
            "relationship": "guardian",
            "phone": "01326571634"
        }
    }'
),
(
    102,
    'Abir',
    '{
        "emergency_contact": {
            "name": "Shahed",
            "relationship": "self",
            "phone": "01912560967"
        }
    }'
),
(
    103,
    'Imam',
    '{
        "emergency_contact": {
            "name": "Hasan",
            "relationship": "guardian",
            "phone": "013267899"
        }
    }'
);

SELECT * FROM student 
WHERE profile @> '{"emergency_contact": {"phone": "01326571634"}}';

SELECT * FROM student 
WHERE name = 'ALIF'