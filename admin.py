from flask import Blueprint, flash, g, redirect, render_template, request, session, url_for
from db import get_db, query_db
import datetime


bp = Blueprint("admin", __name__)


# horribly insecure
# just like me
@bp.route("/admin", methods=["GET", "POST"])
def admin_view():
    # literally just redirect to index if
    #   a. the user is not logged in
    #   b. if logged in, the user is not me

    if request.method == "POST":
        name = request.form["name"]
        body = request.form["body"]
        output = request.form["output"]

        db = get_db()
        now = datetime.datetime.now().strftime("%I:%M:%S%p, %m-%d-%y")
        db.execute("INSERT INTO labs (title, body, output, created) VALUES (?, ?, ?, ?)",
                   (name, body, output, now))

        db.commit()

        return redirect(url_for("index"))

    # oh god why
    if request.method == "GET":
        if "user_id" in session:
            if session["user_id"] == 1:
                print("Redirecting to admin page.")
                return render_template("admin.html")
            else:
                print("User logged in, but is not admin user.")
                return redirect(url_for("index"))
        else:
            print("User not logged in.")
            return redirect(url_for("index"))


