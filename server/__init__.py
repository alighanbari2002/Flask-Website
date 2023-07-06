from flask import Flask, render_template, request, redirect, url_for
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__, static_folder='assets')
auth = HTTPBasicAuth()

users = {
    "ali":    generate_password_hash("ali.password"),
    "behrad": generate_password_hash("behrad.password"),
    "javad":  generate_password_hash("javad.password"),
    "sajad":  generate_password_hash("sajad.password"),
}

@auth.verify_password
def verify_password(username, password):
    if username in users and \
            check_password_hash(users.get(username), password):
        return username


@app.route('/')
@auth.login_required
def index():
    return render_template('actions.html', current_user = auth.current_user())


@app.route('/<user>/Choose_disease')
@auth.login_required
def menu(user):
    print(user)
    # {'WWW-Authenticate': 'Basic realm="Login required"'}
    # return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
