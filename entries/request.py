import sqlite3
import json
from sqlite3 import dbapi2
from models import Entry, Mood, Instructor

def get_all_entries():
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
            m.label,
            i.first_name,
            i.last_name
        FROM entries e
        JOIN moods m
            ON m.id = e.mood_id
        JOIN instructors i 
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

        db_cursor = conn.cursor()

        db_cursor.execute(""" 
        INSERT INTO entries
            (date, concept, entry, mood_id)
        VALUES
            (?,?,?,?)
        """, (
            new_entry["date"],
            new_entry["concept"],
            new_entry["entry"],
            new_entry["moodId"]
        ))

        id = db_cursor.lastrowid

        new_entry["id"] = id

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

