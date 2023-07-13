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

insert_query = """INSERT INTO packages (disease, start_date, finish_date, hospital, doctor, location, cost)
                  VALUES (?, ?, ?, ?, ?, ?, ?);
               """

for i in range(43):
    data = (
        "Influenza",
        "2023-06-01",
        "2023-07-01",
        "Akbar Abadi Hospital",
        "Dr. Moradi",
        "Tehran",
        "11 M",
    )
    if i == 0:
        data = (
            "Influenza",
            "2023-06-01",
            "2023-07-01",
            "Akbari Hospital",
            "Dr. Moradi",
            "Tehran",
            "8 M",
        )
    elif i == 1:
        data = (
            "Facelift",
            "2023-04-15",
            "2023-05-15",
            "Imam Hossein Hospital" "Dr. Shadabi",
            "Dr. Shafei",
            "Tehran",
            "14 M",
        )
    elif i == 2:
        data = (
            "Malaria",
            "2023-03-10",
            "2023-04-10",
            "Sina Hospital",
            "Dr. Mansuri",
            "Tehran",
            "9 M",
        )
    elif i == 3:
        data = (
            "HairTransplant",
            "2023-02-20",
            "2023-03-20",
            "Farabi Hospital",
            "Dr. Saberi",
            "Tehran",
            "18 M",
        )
    elif i == 4:
        data = (
            "Stroke",
            "2023-05-05",
            "2023-06-05",
            "Bahar Loo Hospital",
            "Dr. Rakhshan",
            "Tehran",
            "15 M",
        )
    elif i == 5:
        data = (
            "CysticFibrosis",
            "2023-03-15",
            "2023-04-15",
            "Bahrami Hospital",
            "Dr. Faraji",
            "Tehran",
            "12 M",
        )
    elif i == 6:
        data = (
            "Depression",
            "2023-07-01",
            "2023-08-01",
            "15 Khordad Hospital",
            "Dr. Hejazi",
            "Tehran",
            "8 M",
        )
    elif i == 7:
        data = (
            "BipolarDisorder",
            "2023-06-10",
            "2023-07-10",
            "Tajrish Hospital",
            "Dr. Afrashi",
            "Tehran",
            "14 M",
        )
    elif i == 8:
        data = (
            "AnxietyDisorders",
            "2023-04-20",
            "2023-05-20",
            "Shahid Rajaei Hospital",
            "Dr. Fatehi",
            "Tehran",
            "7 M",
        )

    elif i == 9:
        data = (
            "BreastCancer",
            "2023-07-15",
            "2023-08-15",
            "Razi Hospital",
            "Dr. Vahidi",
            "Tehran",
            "16 M",
        )
    elif i == 10:
        data = (
            "ProstateCancer",
            "2023-05-25",
            "2023-06-25",
            "Rozbeh Hospital",
            "Dr. Saeidi",
            "Tehran",
            "15 M",
        )
    elif i == 11:
        data = (
            "Influenza",
            "2023-07-15",
            "2023-07-20",
            "Razi Hospital",
            "Dr. Elmi",
            "Tehran",
            "10 M",
        )
    elif i == 12:
        data = (
            "Tuberculosis",
            "2023-08-01",
            "2023-08-30",
            "Markazi Hospital",
            "Dr. Saadati",
            "Tehran",
            "9 M",
        )
    elif i == 13:
        data = (
            "Malaria",
            "2023-09-10",
            "2023-09-25",
            "Imam Hospital",
            "Dr. Ghanbari",
            "Tehran",
            "7 M",
        )
    elif i == 14:
        data = (
            "Alzheimer",
            "2023-07-18",
            "2023-08-10",
            "City Hospital",
            "Dr. Maghsoudloo",
            "Tehran",
            "12 M",
        )
    elif i == 15:
        data = (
            "Stroke",
            "2023-08-05",
            "2023-08-25",
            "Rezvan Hospital",
            "Dr. Hosseini",
            "Tehran",
            "12 M",
        )
    elif i == 16:
        data = (
            "Epilepsy",
            "2023-09-15",
            "2023-10-05",
            "Touba Clinic",
            "Dr. Maleki",
            "Tehran",
            "9 M",
        )
    elif i == 17:
        data = (
            "Depression",
            "2023-07-20",
            "2023-08-15",
            "Sina Hospital",
            "Dr. Besharati",
            "Tehran",
            "8 M",
        )
    elif i == 18:
        data = (
            "BipolarDisorder",
            "2023-08-10",
            "2023-09-05",
            "15 Khordad Hospital",
            "Dr. Mehrparvar",
            "Tehran",
            "13 M",
        )
    elif i == 19:
        data = (
            "AnxietyDisorders",
            "2023-09-25",
            "2023-10-20",
            "Touba Clinic",
            "Dr. Hasanloo",
            "Tehran",
            "7 M",
        )
    elif i == 20:
        data = (
            "BreastCancer",
            "2023-07-22",
            "2023-08-30",
            "Markazi Hospital",
            "Dr. Karimi",
            "Tehran",
            "15 M",
        )
    elif i == 21:
        data = (
            "LungCancer",
            "2023-08-12",
            "2023-09-20",
            "General Hospital",
            "Dr. Mellati",
            "Tehran",
            "18 M",
        )
    elif i == 22:
        data = (
            "ProstateCancer",
            "2023-09-01",
            "2023-10-10",
            "Salamat Clinic",
            "Dr. Eskandari",
            "Tehran",
            "13 M",
        )
    elif i == 23:
        data = (
            "ColorectalCancer",
            "2023-07-25",
            "2023-08-25",
            "Bahar Loo Hospital",
            "Dr. Fakharian",
            "Tehran",
            "14000",
        )
    elif i == 24:
        data = (
            "DownSyndrome",
            "2023-09-05",
            "2023-09-30",
            "Soleimani Hospital",
            "Dr. Vatandoost",
            "Tehran",
            "7 M",
        )
    elif i == 25:
        data = (
            "CysticFibrosis",
            "2023-07-28",
            "2023-08-20",
            "Doosti Hospital",
            "Dr. Rakhshan",
            "Tehran",
            "9 M",
        )
    elif i == 26:
        data = (
            "Hemophilia",
            "2023-08-15",
            "2023-09-10",
            "Shahid Bakeri Hospital",
            "Dr. Rezvani",
            "Tehran",
            "12 M",
        )
    elif i == 27:
        data = (
            "HuntingtonDisease",
            "2023-09-01",
            "2023-09-25",
            "Shahid Ahmadi Roshan Hospital",
            "Dr. Ahmadi",
            "Tehran",
            "10 M",
        )
    elif i == 28:
        data = (
            "Botox",
            "2023-07-20",
            "2023-08-10",
            "City Hospital",
            "Dr. Naghizadeh",
            "Tehran",
            "6.5 M",
        )
    elif i == 29:
        data = (
            "HairTransplant",
            "2023-08-05",
            "2023-08-25",
            "Latifi Hospital",
            "Dr. Pooriani",
            "Tehran",
            "8 M",
        )
    elif i == 30:
        data = (
            "BreastAugmentation",
            "2023-09-15",
            "2023-10-05",
            "Rozbeh Clinic",
            "Dr. Mozaffari",
            "Tehran",
            "10 M",
        )
    elif i == 31:
        data = (
            "Facelift",
            "2023-07-22",
            "2023-08-30",
            "Entezari Hospital",
            "Dr. Majidi",
            "Tehran",
            "12 M",
        )
    elif i == 32:
        data = (
            "Influenza",
            "2023-08-12",
            "2023-09-20",
            "Shariat Hospital",
            "Dr. Mortazavi",
            "Tehran",
            "6 M",
        )
    elif i == 33:
        data = (
            "Tuberculosis",
            "2023-09-01",
            "2023-10-10",
            "Bahrami Clinic",
            "Dr. Yousefi",
            "Tehran",
            "9 M",
        )
    elif i == 34:
        data = (
            "Alzheimer",
            "2023-08-15",
            "2023-09-15",
            "Soltani Hospital",
            "Dr. Rajabi",
            "Tehran",
            "10 M",
        )
    elif i == 35:
        data = (
            "Epilepsy",
            "2023-07-22",
            "2023-08-30",
            "Hashemi Hospital",
            "Dr. Safari",
            "Tehran",
            "9000",
        )
    elif i == 36:
        data = (
            "LungCancer",
            "2023-09-01",
            "2023-09-25",
            "Setayesh Clinic",
            "Dr. Mazhari",
            "Tehran",
            "18 M",
        )
    elif i == 37:
        data = (
            "ColorectalCancer",
            "2023-08-12",
            "2023-09-20",
            "Hamedani Hospital",
            "Dr. Moradi",
            "Tehran",
            "14 M",
        )
    elif i == 38:
        data = (
            "Leukemia",
            "2023-09-01",
            "2023-10-10",
            "Shariat Clinic",
            "Dr. Esfehani",
            "Tehran",
            "12 M",
        )
    elif i == 39:
        data = (
            "DownSyndrome",
            "2023-07-25",
            "2023-08-25",
            "Ofogh Hospital",
            "Dr. Vosughi",
            "Tehran",
            "7 M",
        )
    elif i == 40:
        data = (
            "Hemophilia",
            "2023-09-01",
            "2023-09-25",
            "Resalat Clinic",
            "Dr. Eshgi Movahhed",
            "Tehran",
            "12 M",
        )
    elif i == 41:
        data = (
            "Botox",
            "2023-08-15",
            "2023-09-15",
            "Arya Hospital",
            "Dr. Sotoudeh",
            "Tehran",
            "9 M",
        )
    elif i == 42:
        data = (
            "BreastAugmentation",
            "2023-06-01",
            "2023-07-01",
            "Akbar Abadi Hospital",
            "Dr. Moradi",
            "Tehran",
            "11 M",
        )
    cursor.execute(insert_query, data)
    conn.commit()


cursor.close()
conn.close()
