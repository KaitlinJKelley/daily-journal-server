CREATE TABLE 'Entries' (
    'id'    INTEGER PRIMARY KEY AUTOINCREMENT,
    'date'  DATE,
    'concept'    VARCHAR,
    'entry'     VARCHAR,
    'mood_id'   INT,
    'instructor_id'     INT,
    FOREIGN KEY(`mood_id`) REFERENCES `Moods`(`id`),
    FOREIGN KEY(`instructor_id`) REFERENCES `Instructors`(`id`)
);

CREATE TABLE 'Moods' (
    'id' INTEGER PRIMARY KEY AUTOINCREMENT,
    'label' VARCHAR
);

CREATE TABLE 'Instructors' (
    'id'    INTEGER PRIMARY KEY AUTOINCREMENT,
    'first_name'    VARCHAR,
    'last_name'     VARCHAR
);

CREATE TABLE 'Tags' (
    'id'    INTEGER PRIMARY KEY AUTOINCREMENT,
    'subject'   VARCHAR UNIQUE
);

CREATE TABLE 'Entry_Tags' (
    'id'    INTEGER PRIMARY KEY AUTOINCREMENT,
    'entry_id'  INT,
    'tag_id'    INT,
    FOREIGN KEY(`entry_id`) REFERENCES `Entries`(`id`),
    FOREIGN KEY(`tag_id`) REFERENCES `Tags`(`id`)
);

INSERT INTO entries 
    ('date', 'concept', 'entry', 'mood_id', 'instructor_id')
    VALUES ('2021-03-16', 'React', 'React is hard', 3, 1),
            ('2021-04-16', 'Python', 'I miss React', 3, 3);

INSERT INTO Moods
    ('label')
    VALUES ('I got this!'),
            ('Meh'),
            ('Help!');

INSERT INTO instructors
    ('first_name', 'last_name')
    VALUES ('Hannah', 'Hall'),
            ('Scott', 'Silver'),
            ('Adam', 'Sheaffer');

DROP TABLE Moods;

SELECT 
            i.id,
            i.first_name,
            i.last_name
        FROM instructors i;

INSERT INTO Entry_Tags
    ('entry_id', 'tag_id')
VALUES 
    (1, 1),
    (1, 4),
    (1,2),
    (2,3),
    (3,4),
    (3,1);

SELECT DISTINCT
            e.id,
            e.date,
            e.concept,
            e.entry,
            e.mood_id,
            e.instructor_id,
            m.label,
            i.first_name,
            i.last_name
        FROM entries e
        JOIN moods m
            ON m.id = e.mood_id
        LEFT JOIN instructors i
            ON i.id = e.instructor_id
        ;

INSERT INTO Tags
    ('subject')
VALUES  
    ('Debugging'),
    ('React'),
    ('Ask-for-help'),
    ('Not-bad');


SELECT * FROM Tags;

SELECT id, subject 
        FROM Tags t
        WHERE t.subject in ('React',)
        ;