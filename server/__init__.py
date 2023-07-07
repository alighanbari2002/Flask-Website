from flask import Flask, render_template, request, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3

app = Flask(__name__, static_folder="assets")

users = [
    ["ali", generate_password_hash("ali.password"), False],
    ["behrad", generate_password_hash("behrad.password"), False],
    ["javad", generate_password_hash("javad.password"), False],
    ["sajad", generate_password_hash("sajad.password"), True],
]

WRONG_PASSWORD = -1
USER_UNDEFINED = -2
DEAFAULT_VALUE = -3


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
    return -1


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
    return render_template("actions.html", current_user=user, role=get_role(user))


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


@app.route("/<user>/<disease>/choose_package")
def request_cure_package(user, disease):
    conn = sqlite3.connect("E:\\Web-Development\\server\\database\\cure_packages.db")
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
    if request.method == "POST":
        action = request.form.get("action")
        if action == "Submit":
            # Submit button was clicked
            # Perform submit action here
            print("Form submitted!")
        elif action == "Cancel":
            # Cancel button was clicked
            # Perform cancel action here
            print("Form canceled!")
        else:
            # No button was clicked or unknown action
            return "Unknown action!"
    package_id = request.args.get("package", default=-1, type=int)
    return render_template(
        "form.html",
        current_user=user,
        selected_disease=disease,
    )


if __name__ == "__main__":
    app.run(debug=True)
