import sqlite3

conn = sqlite3.connect("patients.db")

cursor = conn.cursor()

cursor.execute(
    """CREATE TABLE datas(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    firstname TEXT,
    lastname TEXT,
    country TEXT,
    zipcode INTEGER,
    diseases TEXT,
    extra_description TEXT,
    evidence_path TEXT,
    supporter TEXT
);"""
)
conn.commit()

cursor.close()
conn.close()
