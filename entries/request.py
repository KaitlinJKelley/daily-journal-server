import sqlite3
import json
from sqlite3 import dbapi2
from models import Entry

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
            e.instructor_id
        FROM entries e
        """)

        entries = []

        dataset = db_cursor.fetchall()

        for row in dataset:
            entry = Entry(row["id"], row["date"], row["concept"], row["entry"], row["mood_id"], row["instructor_id"])

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
            e.instructor_id
        FROM entries e
        WHERE e.id = ?
        """, (id,))

        data = db_cursor.fetchone()

        entry = Entry(data["id"], data["date"], data["concept"], data["entry"], data["mood_id"], data["instructor_id"])

    return json.dumps(entry.__dict__)

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
            e.instructor_id
        FROM entries e
        WHERE e.entry LIKE '%'||?||'%'
        """, (word,))

        dataset = db_cursor.fetchall()

        entries = []

        for row in dataset:
            entry = Entry(row["id"], row["date"], row["concept"], row["entry"], row["mood_id"], row["instructor_id"])

            entries.append(entry.__dict__)
        
        return json.dumps(entries)