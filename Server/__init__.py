from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    send_from_directory,
)
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3, os

app = Flask(__name__, static_folder="assets")
app.config["DOCS_FOLDER"] = os.path.join(
    os.path.join(os.getcwd(), "Server"), "patient documents"
)

users = [
    ["ali", generate_password_hash("ali.password"), False],
    ["behrad", generate_password_hash("behrad.password"), False],
    ["javad", generate_password_hash("javad.password"), False],
    ["sajad", generate_password_hash("sajad.password"), True],
]

WRONG_PASSWORD = -1
USER_UNDEFINED = -2
DEAFAULT_VALUE = -3


def assign_supporter():
    conn = sqlite3.connect("./server/databases/supporters.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM mentors ORDER BY student_cnt ASC")
    freest_supporter = list(cursor.fetchone())
    cursor.execute(
        "UPDATE mentors SET student_cnt = ? WHERE id = ?",
        (freest_supporter[2] + 1, freest_supporter[0]),
    )
    conn.commit()
    cursor.close()
    conn.close()
    return freest_supporter[1]


def to_announce(user):
    conn = sqlite3.connect("./server/databases/patients.db")
    cursor = conn.cursor()
    query = "SELECT id, diseases, evidence_path FROM datas WHERE supporter IS NOT NULL AND user = ? AND is_announced = ?"
    cursor.execute(query, (user, 0))
    unannounced_messages = cursor.fetchall()
    for i in range(len(unannounced_messages)):
        cursor.execute(
            "UPDATE datas SET is_announced = ? WHERE id = ?",
            (1, list(unannounced_messages[i])[0]),
        )
        conn.commit()
    cursor.close()
    conn.close()
    unannounced_messages.reverse()
    return unannounced_messages


def get_role(username):
    for i in range(len(users)):
        if users[i][0] == username:
            return users[i][2]
    return "user do not exit!"


def verify_password(username, password):
    for i in range(len(users)):
        if users[i][0] == username:
            if check_password_hash(users[i][1], password):
                return i
            else:
                return WRONG_PASSWORD
    return USER_UNDEFINED


@app.route("/", methods=["POST", "GET"])
def login():
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
        return redirect(url_for("verify_document", user=user))
    message = request.args.get("message", default=0, type=int)
    return render_template(
        "actions.html",
        current_user=user,
        is_message=message,
    )


@app.route("/<user>/notifications")
def notifications(user):
    persons = to_announce(user)
    is_empty = 0
    if len(persons) == 0:
        is_empty = 1
    return render_template(
        "notifications.html",
        unannounced_messages=persons,
        is_empty=is_empty,
    )


@app.route("/<user>/choose_disease")
def choose_disease(user):
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
        referrer = request.headers.get("Referer")
        if referrer and referrer == request.url:
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
                file_name = "!"
                if file:
                    file_name = (
                        user
                        + "(user)_"
                        + disease
                        + ("(disease)_")
                        + str(package_id)
                        + ("(packageId)")
                        + "."
                        + file.filename.rsplit(".", 1)[1]
                    )
                    file_path = app.config["DOCS_FOLDER"] + "/" + file_name
                    file.save(file_path)

                conn = sqlite3.connect("./server/databases/patients.db")
                cursor = conn.cursor()
                insert_query = """
                    INSERT INTO datas (user, firstname, lastname, country, zipcode, diseases, extra_description, evidence_path, is_announced)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)"""
                data = (
                    user,
                    firstname,
                    lastname,
                    country,
                    zipcode,
                    disease,
                    extraDescription,
                    file_name,
                    0,
                )
                cursor.execute(insert_query, data)
                conn.commit()
                cursor.close()
                conn.close()
                return redirect(url_for("menu", user=user, message=1))
        return redirect(url_for("menu", user=user, message=0))

    return render_template(
        "form.html",
        current_user=user,
        selected_disease=disease,
        package_id=package_id,
    )


@app.route("/download_file/<path:filename>", methods=["POST", "GET"])
def download_file(filename):
    documents = os.path.join(app.root_path, app.config["DOCS_FOLDER"])
    return send_from_directory(documents, filename, as_attachment=True)


@app.route("/<user>/verify_document", methods=["POST", "GET"])
def verify_document(user):
    if request.method == "POST":
        referrer = request.headers.get("Referer")
        if referrer and referrer == request.url:
            patient_id = request.form["patient_id"]
            conn = sqlite3.connect("./server/databases/patients.db")
            cursor = conn.cursor()
            query = "UPDATE datas SET supporter = ? WHERE id = ?"
            cursor.execute(query, (assign_supporter(), patient_id))
            conn.commit()
            cursor.close()
            conn.close()
            return redirect(url_for("verify_document", user=user))

    conn = sqlite3.connect("./server/databases/patients.db")
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id, firstname, lastname, country, zipcode, diseases, extra_description, evidence_path FROM datas WHERE supporter IS NULL"
    )
    unverified_docs = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template("verify.html", current_user=user, docs=unverified_docs)


if __name__ == "__main__":
    app.run(debug=True, port=5000, host="127.0.0.1")
