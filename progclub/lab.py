from subprocess import check_output
from flask import Blueprint, flash, g, redirect, render_template, request, session, url_for
from werkzeug.exceptions import abort
from werkzeug.utils import secure_filename
from .db import get_db, query_db

bp = Blueprint("labs", __name__, url_prefix="/labs")


@bp.route("/<int:id>", methods=("GET", "POST"))
def lab(id):
    lab = query_db("select * from labs where id = ?", (id,), True)

    navbar = render_template("default_navbar.html")
    # weird fix but ok
    # fix later
    if "user_id" in session:
        navbar = render_template("user_navbar.html", username=session["username"])

    if request.method == "POST":

        # Check whether or not the user is logged in.
        user = getattr(g, "user", None)

        if session["user_id"] is None:
            print("No user found in this session. Redirecting...")
            return redirect(url_for("auth.login"))

        # If logged in, continue.
        else:
            file = request.files["fileupload"]

            if file.filename == "":
                print("Empty filename.")

            if file:
                filename = secure_filename(file.filename)
                extension = filename[filename.index("."):]
                file.save(filename)

                user_output = check_output("python " + filename, shell=True).decode("utf-8")
                print(user_output)

                # return result somehow
                flash("Yay! Looks like your output was correct!")
                return render_template("lab.html", title=lab["title"], body=lab["body"], navbar=navbar)

    return render_template("lab.html", title=lab["title"], body=lab["body"], navbar=navbar)

