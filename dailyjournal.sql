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
    'subject'   VARCHAR
);

CREATE TABLE 'EntryTags' (
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