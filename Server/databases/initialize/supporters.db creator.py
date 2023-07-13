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

insert_query = """INSERT INTO mentors (name, student_cnt)
                  VALUES (?, ?);
               """

for i in range(5):
    data = (
        "Pouya Fekri",
        "0",
    )
    if i == 0:
        data = (
            "Pouya Fekri",
            "0",
        )
    elif i == 1:
        data = (
            "Mohammad sajad Naghizadeh",
            "0",
        )
    elif i == 2:
        data = (
            "Soudabeh Mohammad hashemi",
            "0",
        )
    elif i == 3:
        data = (
            "Arash Mohammad poor",
            "0",
        )
    elif i == 4:
        data = (
            "Matin Zamani",
            "0",
        )

    cursor.execute(insert_query, data)
    conn.commit()

cursor.close()
conn.close()
