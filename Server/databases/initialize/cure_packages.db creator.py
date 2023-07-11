import sqlite3

conn = sqlite3.connect("cure_packages.db")

cursor = conn.cursor()

cursor.execute(
    """CREATE TABLE packages(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    disease TEXT NOT NULL,
    start_date TEXT NOT NULL,
    finish_date TEXT NOT NULL,
    hospital TEXT NOT NULL,
    doctor TEXT NOT NULL,
    location TEXT NOT NULL,
    cost TEXT NOT NULL,
    patient TEXT
);"""
)

conn.commit()

for i in range(11):
    sqlite_insert_query = """INSERT INTO packages (disease, start_date, finish_date, hospital, doctor, location, cost)
VALUES ('Influenza', '2023-06-01', '2023-07-01', 'Akhtar Hospital', 'Dr. Heydari', 'Tehran', '10 M');
"""
    if i == 0:
        sqlite_insert_query = """INSERT INTO packages (disease, start_date, finish_date, hospital, doctor, location, cost)
VALUES ('Influenza', '2023-06-01', '2023-07-01', 'Akbar Abadi Hospital', 'Dr. Moradi', 'Tehran', '11 M');
"""
    elif i == 1:
        sqlite_insert_query = """INSERT INTO packages (disease, start_date, finish_date, hospital, doctor, location, cost)
VALUES ('Facelift', '2023-04-15', '2023-05-15', 'Imam Hossein Hospital', 'Dr. Shadabi', 'Tehran', '14 M');
"""
    elif i == 2:
        sqlite_insert_query = """INSERT INTO packages (disease, start_date, finish_date, hospital, doctor, location, cost)
VALUES ('Malaria', '2023-03-10', '2023-04-10', 'Sina Hospital', 'Dr. Mansuri', 'Tehran', '9 M');
"""
    elif i == 3:
        sqlite_insert_query = """INSERT INTO packages (disease, start_date, finish_date, hospital, doctor, location, cost)
VALUES ('HairTransplant', '2023-02-20', '2023-03-20', 'Farabi Hospital', 'Dr. Saberi', 'Tehran', '18 M');
"""
    elif i == 4:
        sqlite_insert_query = """INSERT INTO packages (disease, start_date, finish_date, hospital, doctor, location, cost)
VALUES ('Stroke', '2023-05-05', '2023-06-05', 'Bahar Loo Hospital', 'Dr. Rakhshan', 'Tehran', '15 M');
"""
    elif i == 5:
        sqlite_insert_query = """INSERT INTO packages (disease, start_date, finish_date, hospital, doctor, location, cost)
VALUES ('CysticFibrosis', '2023-03-15', '2023-04-15', 'Bahrami Hospital', 'Dr. Faraji', 'Tehran', '12 M');
"""
    elif i == 6:
        sqlite_insert_query = """INSERT INTO packages (disease, start_date, finish_date, hospital, doctor, location, cost)
VALUES ('Depression', '2023-07-01', '2023-08-01', '15 Khordad Hospital', 'Dr. Hejazi', 'Tehran', '8 M');
"""
    elif i == 7:
        sqlite_insert_query = """INSERT INTO packages (disease, start_date, finish_date, hospital, doctor, location, cost)
VALUES ('BipolarDisorder', '2023-06-10', '2023-07-10', 'Tajrish Hospital', 'Dr. Afrashi', 'Tehran', '14 M');
"""
    elif i == 8:
        sqlite_insert_query = """INSERT INTO packages (disease, start_date, finish_date, hospital, doctor, location, cost)
VALUES ('AnxietyDisorders', '2023-04-20', '2023-05-20', 'Shahid Rajaei Hospital', 'Dr. Fatehi', 'Tehran', '7 M');
"""
    elif i == 9:
        sqlite_insert_query = """INSERT INTO packages (disease, start_date, finish_date, hospital, doctor, location, cost)
VALUES ('BreastCancer', '2023-07-15', '2023-08-15', 'Razi Hospital', 'Dr. Vahidi', 'Tehran', '16 M');
"""
    elif i == 10:
        sqlite_insert_query = """INSERT INTO packages (disease, start_date, finish_date, hospital, doctor, location, cost)
VALUES ('ProstateCancer', '2023-05-25', '2023-06-25', 'Rozbeh Hospital', 'Dr. Saeidi', 'Tehran', '15 M');
"""

    cursor.execute(sqlite_insert_query)
    conn.commit()


cursor.close()
conn.close()
