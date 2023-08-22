from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    send_from_directory,
)
from werkzeug.security import check_password_hash, generate_password_hash
import sqlite3, os

app = Flask(__name__, static_folder="assets")

app.config["DOCS_FOLDER"] = os.path.join(
    os.path.join(os.getcwd(), "Server"), "patient documents"
)

USER = 0
VERIFIER = 1
USER_UNDEFINED = -1
WRONG_PASSWORD = -2
NOTTHING = -3

logged_in_users = {}


def assign_supporter():
    conn = sqlite3.connect("./Server/databases/supporters.db")
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
    conn = sqlite3.connect("./Server/databases/patients.db")
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


def login_validation(username, password):
    conn = sqlite3.connect("./Server/databases/users.db")
    cursor = conn.cursor()
    query = "SELECT id, password, role FROM userInfo WHERE username = ?"
    cursor.execute(query, (username,))
    user = cursor.fetchone()
    cursor.close()
    conn.close()
    if user is None:
        return USER_UNDEFINED, NOTTHING
    elif check_password_hash(user[1], password):
        return user[0], user[2]
    else:
        return WRONG_PASSWORD, NOTTHING


def signup_validation(username):
    conn = sqlite3.connect("./Server/databases/users.db")
    cursor = conn.cursor()
    query = "SELECT id FROM userInfo WHERE username = ?"
    cursor.execute(query, (username,))
    user = cursor.fetchone()
    cursor.close()
    conn.close()
    if user is None:
        return USER_UNDEFINED
    else:
        return user[0]


def not_logged_in(user):
    if user not in logged_in_users:
        return True
    elif logged_in_users[user] is False:
        return True
    return False


@app.route("/favicon.ico")
def favicon():
    return send_from_directory(
        os.path.join(app.root_path, "assets"),
        "favicon.ico",
        mimetype="image/vnd.microsoft.icon",
    )


@app.route("/", methods=["POST", "GET"])
def login():
    message = request.args.get("message", default=0, type=int)
    status = 0
    if request.method == "POST":
        username = request.form["Username"]
        password = request.form["Password"]
        status, role = login_validation(username, password)
        if status > 0:
            logged_in_users[username] = True
            if role == USER:
                return redirect(url_for("menu", user=username))
            elif role == VERIFIER:
                return redirect(url_for("verify_document", user=username))
    return render_template("login.Jinja2", stat=status, is_message=message)


@app.route("/signup", methods=["POST", "GET"])
def signup():
    status = 0
    if request.method == "POST":
        username = request.form["Username"]
        password = request.form["Password"]
        status = signup_validation(username)
        if status == USER_UNDEFINED:
            logged_in_users[username] = True
            conn = sqlite3.connect("./Server/databases/users.db")
            cursor = conn.cursor()
            insert_query = """INSERT INTO userInfo (username, password, role)
                              VALUES (?, ?, ?);
                           """
            cursor.execute(
                insert_query, (username, generate_password_hash(password), USER)
            )
            conn.commit()
            cursor.close()
            conn.close()
            return redirect(url_for("menu", user=username))
    return render_template("signup.Jinja2", stat=status)


@app.route("/<user>")
def panel(user):
    if not_logged_in(user):
        return redirect(url_for("login", message=1))
    return redirect(url_for("menu", user=user))


@app.route("/<user>/logout")
def logout(user):
    if not_logged_in(user):
        return redirect(url_for("login", message=1))
    logged_in_users[user] = False
    return redirect(url_for("login"))


@app.route("/<user>/menu")
def menu(user):
    if not_logged_in(user):
        return redirect(url_for("login", message=1))
    message = request.args.get("message", default=0, type=int)
    return render_template(
        "actions.Jinja2",
        current_user=user,
        is_message=message,
    )


@app.route("/<user>/notifications")
def notifications(user):
    if not_logged_in(user):
        return redirect(url_for("login", message=1))
    persons = to_announce(user)
    is_empty = 0
    if len(persons) == 0:
        is_empty = 1
    return render_template(
        "notifications.Jinja2",
        unannounced_messages=persons,
        is_empty=is_empty,
    )


@app.route("/<user>/choose_disease")
def choose_disease(user):
    if not_logged_in(user):
        return redirect(url_for("login", message=1))
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
        "diseases.Jinja2", diseases=covered_diseases, current_user=user
    )


@app.route("/<user>/<disease>/choose_package", methods=["POST", "GET"])
def choose_package(user, disease):
    if not_logged_in(user):
        return redirect(url_for("login", message=1))
    if request.method == "POST":
        package_id = request.form["package"]
        return redirect(
            url_for("fill_out_form", user=user, disease=disease, package_id=package_id)
        )
    else:
        conn = sqlite3.connect("./Server/databases/cure_packages.db")
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
            "packages.Jinja2",
            packages=available_packages,
            current_user=user,
            selected_disease=disease,
            is_empty=is_empty,
        )


@app.route("/<user>/<disease>/fill_out_form", methods=["POST", "GET"])
def fill_out_form(user, disease):
    if not_logged_in(user):
        return redirect(url_for("login", message=1))
    package_id = request.args.get("package_id", default=-1, type=int)
    if request.method == "POST":
        referrer = request.headers.get("Referer")
        if referrer and referrer == request.url:
            action = request.form["action"]
            if action == "Submit":
                conn = sqlite3.connect("./Server/databases/cure_packages.db")
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

                conn = sqlite3.connect("./Server/databases/patients.db")
                cursor = conn.cursor()
                insert_query = """
                                  INSERT INTO datas (user, firstname, lastname, country, zipcode, diseases, extra_description, evidence_path, is_announced)
                                  VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                               """
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
        "form.Jinja2",
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
    if not_logged_in(user):
        return redirect(url_for("login", message=1))
    if request.method == "POST":
        referrer = request.headers.get("Referer")
        if referrer and referrer == request.url:
            patient_id = request.form["patient_id"]
            conn = sqlite3.connect("./Server/databases/patients.db")
            cursor = conn.cursor()
            query = "UPDATE datas SET supporter = ? WHERE id = ?"
            cursor.execute(query, (assign_supporter(), patient_id))
            conn.commit()
            cursor.close()
            conn.close()
            return redirect(url_for("verify_document", user=user))

    conn = sqlite3.connect("./Server/databases/patients.db")
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id, firstname, lastname, country, zipcode, diseases, extra_description, evidence_path FROM datas WHERE supporter IS NULL"
    )
    unverified_docs = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template("verify.Jinja2", current_user=user, docs=unverified_docs)


if __name__ == "__main__":
    app.run(debug=True, port=5000, host="127.0.0.1")
