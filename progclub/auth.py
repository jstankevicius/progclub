import functools
from flask import Blueprint, flash, g, redirect, render_template, request, session, url_for
from werkzeug.security import check_password_hash, generate_password_hash
from .db import get_db

bp = Blueprint("auth", __name__, url_prefix="/auth")


@bp.route("/register", methods=("GET", "POST"))
def register():

    # If the user is submitting data, I.E. their registration form, then...
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        db = get_db()

        error = None

        if not username:
            error = "Username is required."
        elif not password:
            error = "Password is required."

        # Look up a user with the same name as the form. If ANYTHING returns, we error out.
        elif db.execute("SELECT id FROM users WHERE username = ?", (username,)).fetchone() is not None:
            print("User is already registered.")
            error = "User {} is already registered.".format(username)

        # If we encounter no errors along the way, process the request:
        if error is None:
            db.execute("INSERT INTO users (username, password) VALUES (?, ?)",
                       (username, generate_password_hash(password)))
            db.commit()
            return redirect(url_for("auth.login"))

        flash(error)

    return render_template("register.html")


@bp.route("/login", methods=("GET", "POST"))
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        db = get_db()

        error = None

        user = db.execute("SELECT * FROM users WHERE username = ?", (username,)).fetchone()

        if user is None:
            error = "Incorrect username"
            print("Incorrect username.")
        elif not check_password_hash(user["password"], password):
            error = "Incorrect password"
            print("Incorrect password.")

        if error is None:
            session.clear()
            session["user_id"] = user["id"]
            session["username"] = user["username"]

            print("Successful login")
            return redirect(url_for("index"))

        flash(error)

    return render_template("login.html")


@bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))