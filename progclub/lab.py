from subprocess import check_output
from flask import Blueprint, flash, g, redirect, render_template, request, session, url_for
from werkzeug.exceptions import abort
from werkzeug.utils import secure_filename
from .db import get_db, query_db

bp = Blueprint("labs", __name__, url_prefix="/labs")


@bp.route("/<int:id>", methods=("GET", "POST"))
def lab(id):

    lab = query_db("select * from labs where id = ?", (id,), True)

    if request.method == "POST":
        file = request.files["fileupload"]

        # Check whether or not the user is logged in.
        user = getattr(g, "user", None)
        if session["user_id"] is None:
            print("No user found in this session. Redirecting...")
            return redirect(url_for("auth.login"))

        # If logged in, continue.
        else:
            if file.filename == "":
                print("Empty filename.")

            if file:
                filename = secure_filename(file.filename)
                extension = filename[filename.index("."):]
                file.save(filename)

                user_output = check_output("python " + filename, shell=True).decode("utf-8")
                correct_output = lab["output"]
                print(user_output)

                # compile code

                # return result somehow

    return render_template("lab.html", title=lab["title"], body=lab["body"])

