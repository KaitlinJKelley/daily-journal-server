import sqlite3
import json
from sqlite3 import dbapi2
from models import Entry, Mood, Instructor, Tag, Entry_Tag

def get_all_entries():
    with sqlite3.connect("dailyjournal.db") as conn:

        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute(""" 
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
        """)

        entries = []

        dataset = db_cursor.fetchall()

        for row in dataset:
            entry = Entry(row["id"], row["date"], row["concept"], row["entry"], row["mood_id"], row["instructor_id"])

            mood = Mood(row["mood_id"], row["label"])
            entry.mood = mood.__dict__

            instructor = Instructor(row["instructor_id"], row["first_name"], row["last_name"])
            entry.instructor = instructor.__dict__

            entries.append(entry.__dict__)

    return json.dumps(entries)

def get_single_entry(id):
    with sqlite3.connect("dailyjournal.db") as conn:

        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute(""" 
        SELECT
            e.id,
            e.date,
            e.concept,
            e.entry,
            e.mood_id,
            e.instructor_id,
            m.label
        FROM entries e
        JOIN moods m
            ON e.mood_id = m.id
        WHERE e.id = ?
        """, (id,))

        data = db_cursor.fetchone()

        entry = Entry(data["id"], data["date"], data["concept"], data["entry"], data["mood_id"], data["instructor_id"])

        mood = Mood(data["mood_id"], data["label"])

        entry.mood = mood.__dict__

    return json.dumps(entry.__dict__)

def create_entry(new_entry):
    with sqlite3.connect("./dailyJournal.db") as conn:
        conn.row_factory = sqlite3.Row 
        db_cursor = conn.cursor()

        # Create Tag if necessary
        db_cursor.execute(""" 
        SELECT 
            t.id, 
            t.subject 
        FROM Tags t
        """)

        all_tags = []

        entry_tags = []
        # Get everything that was returned from the SQL query
        tags_dataset = db_cursor.fetchall()

        for row in tags_dataset:
            # Create a readable instance of each row from the database
            tag = Tag(row["id"], row["subject"])
            all_tags.append(tag.__dict__)
        
        # Converts list into a single string containing all tags from user
        new_entry_tags_joined = " ".join(new_entry["tags"])
        # Converts single string into a list of individual strings representing each tag from the user
        new_entry_tags_sep_list = new_entry_tags_joined.split(",")

        # Iterate over each tag that the user submitted
        for tag in new_entry_tags_sep_list:
            # Iterate over each tag dict in all_tags; if the new_entry tag string doesn't match any of the all_tags subjects, 
            # add that tag to the Tags table
            if tag not in [t["subject"] for t in all_tags]:
                db_cursor.execute(""" 
                INSERT INTO Tags
                    ('subject')
                VALUES
                    (?)
                """, (tag,))

                # Get the most recent id that was added the database
                new_tag_id = db_cursor.lastrowid
                # Create an instance of the newly added tag
                new_tag = Tag(new_tag_id, tag)

                entry_tags.append(new_tag.__dict__)
            else:
                # Loops through the list of tags originally returned from Tags table, 
                # and checks (filters) for the tags that have a subject matching the tag entered by the user
                existing_tags_list =  [t for t in all_tags if tag == t["subject"]]

                entry_tags.extend(existing_tags_list)

        # Create Entry
        db_cursor.execute(""" 
        INSERT INTO entries
            (date, concept, entry, mood_id, instructor_id)
        VALUES
            (?,?,?,?,?)
        """, (
            new_entry["date"],
            new_entry["concept"],
            new_entry["entry"],
            new_entry["moodId"],
            new_entry["instructorId"]
        ))

        id = db_cursor.lastrowid

        new_entry["id"] = id

        # Create Entry_Tag
        # Iterates the list of entry_tags (new and previously existing tags that match user input) to create Entry_Tag rows
        for row in entry_tags:

            db_cursor.execute(""" 
            INSERT INTO entry_tags
                ('tag_id', 'entry_id')
            VALUES
                (?,?)
            """, (row["id"], id))

        return json.dumps(new_entry)

def delete_entry(id):
    with sqlite3.connect("dailyjournal.db") as conn:

        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute(""" 
        DELETE FROM entries
        WHERE id = ?
        """, (id,))

def get_entries_by_word(word):

    with sqlite3.connect("dailyjournal.db") as conn:

        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute(""" 
        SELECT
            e.id,
            e.date,
            e.concept,
            e.entry,
            e.mood_id,
            e.instructor_id,
            m.label
        FROM entries e
        JOIN moods m
            ON e.mood_id = m.id
        WHERE e.entry LIKE '%'||?||'%'
        """, (word,))

        dataset = db_cursor.fetchall()

        entries = []

        for row in dataset:
            entry = Entry(row["id"], row["date"], row["concept"], row["entry"], row["mood_id"], row["instructor_id"])

            mood = Mood(row["mood_id"], row["label"])

            entry.mood = mood.__dict__

            entries.append(entry.__dict__)
        
        return json.dumps(entries)

def update_entry(id, updated_entry):
    
    with sqlite3.connect("./dailyJournal.db") as conn:

        db_cursor = conn.cursor()

        db_cursor.execute(""" 
        UPDATE entries
        SET
            id = ?,
            date = ?,
            concept = ?,
            entry = ?,
            mood_id = ?
        WHERE id = ?
        """, (updated_entry["id"],updated_entry["date"],updated_entry["concept"],updated_entry["entry"],updated_entry["moodId"], id,))

        rows_affected = db_cursor.rowcount

        if rows_affected == 0:
            return False
        else: 
            return True

