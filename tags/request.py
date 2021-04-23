import sqlite3
import json
from sqlite3.dbapi2 import DatabaseError
from models import Tag, Entry_Tag

def get_all_tags():
    with sqlite3.connect("./dailyJournal.db") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute(""" 
        SELECT
            t.id,
            t.subject
        FROM tags t
        """)

        tags = []

        dataset = db_cursor.fetchall()

        for row in dataset:
            tag = Tag(row["id"], row["subject"])

            tags.append(tag.__dict__)
        
        return json.dumps(tags)

def get_all_entry_tags():
    with sqlite3.connect("./dailyJournal.db") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute(""" 
        SELECT
            et.id,
            et.entry_id,
            et.tag_id
        FROM entry_tags et
        """)

        entry_tags = []

        dataset = db_cursor.fetchall()

        for row in dataset:
            entry_tag = Entry_Tag(row["id"], row["entry_id"], row["tag_id"])

            entry_tags.append(entry_tag.__dict__)

        return json.dumps(entry_tags)