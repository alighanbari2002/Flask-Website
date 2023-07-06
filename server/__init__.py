from flask import Flask, render_template, request, redirect, url_for
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3

app = Flask(__name__, static_folder="assets")
auth = HTTPBasicAuth()

users = {
    "ali": generate_password_hash("ali.password"),
    "behrad": generate_password_hash("behrad.password"),
    "javad": generate_password_hash("javad.password"),
    "sajad": generate_password_hash("sajad.password"),
}


@auth.verify_password
def verify_password(username, password):
    if username in users and check_password_hash(users.get(username), password):
        return username


@app.route("/")
@auth.login_required
def index():
    return render_template("actions.html", current_user=auth.current_user())


@app.route("/<user>/Choose_disease")
@auth.login_required
def disease_menu(user):
    covered_diseases = [
        ["Infectious Diseases", ["Influenza", "Tuberculosis", "Malaria"]],
        ["Neurological Disorders", ["Alzheimer", "Stroke", "Epilepsy"]],
        [
            "Mental Health Disorders",
            [
                "Depression",
                "Bipolar_disorder",
                "Anxiety_disorders",
            ],
        ],
        [
            "Cancer",
            [
                "Breast_cancer",
                "Lung_cancer",
                "Prostate_cancer",
                "Colorectal_cancer",
                "Leukemia",
            ],
        ],
        [
            "Genetic Disorders",
            ["Down_syndrome", "Cystic_fibrosis", "Hemophilia", "Huntington_disease"],
        ],
        [
            "plastic surgery",
            ["Botox", "Hair_Transplant", "Breast_Augmentation", "Facelift"],
        ],
    ]
    return render_template(
        "diseases.html", diseases=covered_diseases, current_user=user
    )


@app.route("/<user>/<disease>/request_cure_package")
@auth.login_required
def request_cure_package(user, disease):
    return "" + disease + "   " + user


if __name__ == "__main__":
    app.run(debug=True)


#  return redirect(url_for('user', name = username))
