import sqlite3

conn = sqlite3.connect("patients.db")

cursor = conn.cursor()

cursor.execute(
    """CREATE TABLE datas(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user TEXT NOT NULL,
    firstname TEXT,
    lastname TEXT,
    country TEXT,
    zipcode INTEGER,
    diseases TEXT,
    extra_description TEXT,
    evidence_path TEXT,
    supporter TEXT,
    is_announced INTEGER
);"""
)
conn.commit()

cursor.close()
conn.close()
