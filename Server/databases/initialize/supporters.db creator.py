import sqlite3

conn = sqlite3.connect("supporters.db")

cursor = conn.cursor()

cursor.execute(
    """CREATE TABLE mentors(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    student_cnt INTEGER
);"""
)

conn.commit()

for i in range(5):
    sqlite_insert_query = """INSERT INTO mentors (name, student_cnt)
VALUES ('Pouya Fekri', '0');
"""
    if i == 0:
        sqlite_insert_query = """INSERT INTO mentors (name, student_cnt)
    VALUES ('Pouya Fekri', '0');
    """
    elif i == 1:
        sqlite_insert_query = """INSERT INTO mentors (name, student_cnt)
    VALUES ('Mohammad sajad Naghizadeh', '0');
    """
    elif i == 2:
        sqlite_insert_query = """INSERT INTO mentors (name, student_cnt)
    VALUES ('Soudabeh Mohammad hashemi', '0');
    """
    elif i == 3:
        sqlite_insert_query = """INSERT INTO mentors (name, student_cnt)
    VALUES ('Arash Mohammad poor', '0');
    """
    elif i == 4:
        sqlite_insert_query = """INSERT INTO mentors (name, student_cnt)
    VALUES ('Matin Zamani', '0');
    """
    cursor.execute(sqlite_insert_query)
    conn.commit()

cursor.close()
conn.close()
