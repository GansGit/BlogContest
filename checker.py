import sqlite3


def check_for_name_in_db(username):
    with sqlite3.connect("db.sql") as db:
        cursor = db.cursor()
        cursor.execute(f"SELECT username FROM users WHERE username = '{username}'")
        result = cursor.fetchall()
        if len(result) > 0:
            return True
        else:
            return False
            