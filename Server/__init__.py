from flask import Flask, render_template, request, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3, os

app = Flask(__name__, static_folder="assets")

users = [
    ["ali", generate_password_hash("ali.password"), False],
    ["behrad", generate_password_hash("behrad.password"), False],
    ["javad", generate_password_hash("javad.password"), False],
    ["sajad", generate_password_hash("sajad.password"), True],
]

supporters = [
    "Pouya Fekri",
    "Mohammad sajad Naghizadeh",
    "Soudabeh Mohammad hashemi",
    "Arash Mohammad poor",
    "Matin Zamani",
]


SUPPORTER_INDEX = 0
WRONG_PASSWORD = -1
USER_UNDEFINED = -2
DEAFAULT_VALUE = -3


def calc_supporter_index():
    SUPPORTER_INDEX = (SUPPORTER_INDEX + 1) % len(supporters)
    return SUPPORTER_INDEX


def verify_password(username, password):
    for i in range(len(users)):
        if users[i][0] == username:
            if check_password_hash(users[i][1], password):
                return i
            else:
                return WRONG_PASSWORD
    return USER_UNDEFINED


def get_role(username):
    for i in range(len(users)):
        if users[i][0] == username:
            return users[i][2]
    return "user do not exit!"


@app.route("/", methods=["POST", "GET"])
def index():
    status = DEAFAULT_VALUE
    if request.method == "POST":
        username = request.form["Username"]
        password = request.form["Password"]
        status = verify_password(username, password)
        if status >= 0:
            return redirect(url_for("menu", user=username))
    return render_template("login.html", stat=status)


@app.route("/<user>/menu")
def menu(user):
    is_verifier = get_role(user)
    if is_verifier:
        return redirect(url_for("verify_package", user=user))
    message = request.args.get("message", default=0, type=int)
    return render_template("actions.html", current_user=user, is_message=message)


@app.route("/<user>/choose_disease")
def disease_menu(user):
    covered_diseases = [
        ["Infectious Diseases", ["Influenza", "Tuberculosis", "Malaria"]],
        ["Neurological Disorders", ["Alzheimer", "Stroke", "Epilepsy"]],
        [
            "Mental Health Disorders",
            [
                "Depression",
                "BipolarDisorder",
                "AnxietyDisorders",
            ],
        ],
        [
            "Cancer",
            [
                "BreastCancer",
                "LungCancer",
                "ProstateCancer",
                "ColorectalCancer",
                "Leukemia",
            ],
        ],
        [
            "Genetic Disorders",
            ["DownSyndrome", "CysticFibrosis", "Hemophilia", "HuntingtonDisease"],
        ],
        [
            "plastic surgery",
            ["Botox", "HairTransplant", "BreastAugmentation", "Facelift"],
        ],
    ]
    return render_template(
        "diseases.html", diseases=covered_diseases, current_user=user
    )


@app.route("/<user>/<disease>/choose_package", methods=["POST", "GET"])
def choose_package(user, disease):
    if request.method == "POST":
        package_id = request.form["package"]
        return redirect(
            url_for("fill_out_form", user=user, disease=disease, package_id=package_id)
        )
    else:
        conn = sqlite3.connect("./server/databases/cure_packages.db")
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM packages WHERE patient IS NULL AND disease = ?", (disease,)
        )
        available_packages = cursor.fetchall()
        is_empty = False
        if len(available_packages) == 0:
            is_empty = True
        cursor.close()
        conn.close()

        return render_template(
            "packages.html",
            packages=available_packages,
            current_user=user,
            selected_disease=disease,
            is_empty=is_empty,
        )


@app.route("/<user>/<disease>/fill_out_form", methods=["POST", "GET"])
def fill_out_form(user, disease):
    package_id = request.args.get("package_id", default=-1, type=int)
    if request.method == "POST":
        action = request.form["action"]
        if action == "Submit":
            conn = sqlite3.connect("./server/databases/cure_packages.db")
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE packages SET patient = ? WHERE id = ?", (user, package_id)
            )
            conn.commit()
            cursor.close()
            conn.close()

            firstname = request.form["firstname"]
            lastname = request.form["lastname"]
            country = request.form["country"]
            zipcode = request.form["zipcode"]
            extraDescription = request.form["extraDescription"]
            file = request.files["file"]
            file_path = ""
            if file:
                folder_path = (
                    "./server/patient documents/"
                    + user
                    + "-"
                    + disease
                    + "-"
                    + str(package_id)
                    + " (%user-%disease-%package_id)"
                )
                file_path = folder_path + "/" + file.filename
                os.mkdir(folder_path)
                file.save(file_path)

            conn = sqlite3.connect("./server/databases/patients.db")
            cursor = conn.cursor()
            insert_query = """
                            INSERT INTO datas (firstname, lastname, country, zipcode, diseases, extra_description, evidence_path)
                            VALUES (?, ?, ?, ?, ?, ?, ?)"""
            data = (
                firstname,
                lastname,
                country,
                zipcode,
                disease,
                extraDescription,
                file_path,
            )
            cursor.execute(insert_query, data)
            conn.commit()
            cursor.close()
            conn.close()
            return redirect(url_for("menu", user=user, message=1))
        else:
            return redirect(url_for("menu", user=user, message=0))
    else:
        return render_template(
            "form.html",
            current_user=user,
            selected_disease=disease,
            package_id=package_id,
        )


@app.route("/<user>/verify_package", methods=["POST", "GET"])
def verify_package(user):
    conn = sqlite3.connect("./server/databases/patients.db")
    cursor = conn.cursor()
    cursor.execute(
        "SELECT firstname, lastname, country, zipcode, diseases, extra_description, evidence_path FROM datas WHERE supporter IS NULL"
    )
    rows = cursor.fetchall()
    unverified_packages = []
    for row in rows:
        unverified_packages.append(row)
    cursor.close()
    conn.close()

    print(unverified_packages)
    return render_template("verify.html", packages=unverified_packages)


if __name__ == "__main__":
    app.run(debug=True)


# verify package:

# conn = sqlite3.connect("./server/databases/patients.db")
# cursor = conn.cursor()
# query = "UPDATE datas SET supporter = ? WHERE id = ?"
# cursor.execute(query, (supporters[calc_supporter_index()], id))
# conn.commit()
