import sqlite3
from werkzeug.security import generate_password_hash

conn = sqlite3.connect("users.db")

cursor = conn.cursor()

cursor.execute(
    """CREATE TABLE userInfo(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    password TEXT NOT NULL,
    role INTEGER
);"""
)

conn.commit()


insert_query = """INSERT INTO userInfo (username, password, role)
               VALUES (?, ?, ?);
               """

for i in range(4):
    data = (
        "ali",
        generate_password_hash("ali.password"),
        0,
    )

    if i == 0:
        data = (
            "ali",
            generate_password_hash("ali.password"),
            0,
        )
    elif i == 1:
        data = (
            "behrad",
            generate_password_hash("behrad.password"),
            0,
        )
    elif i == 2:
        data = (
            "javad",
            generate_password_hash("javad.password"),
            0,
        )
    elif i == 3:
        data = (
            "sajad",
            generate_password_hash("sajad.password"),
            1,
        )

    cursor.execute(insert_query, data)
    conn.commit()

cursor.close()
conn.close()
