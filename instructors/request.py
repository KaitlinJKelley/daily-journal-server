import sqlite3
import json
from models import Instructor

def get_all_instructors():
    with sqlite3.connect("./dailyJournal.db") as conn:

        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute(""" 
        SELECT 
            i.id,
            i.first_name,
            i.last_name
        FROM instructors i
        """)

        instructors = []

        dataset = db_cursor.fetchall()

        for row in dataset:
            instructor = Instructor(row["id"], row["first_name"], row["last_name"])

            instructors.append(instructor.__dict__)

        return json.dumps(instructors)