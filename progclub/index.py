from flask import Blueprint, flash, g, redirect, render_template, request, url_for
from werkzeug.exceptions import abort
from werkzeug.utils import secure_filename
from .db import get_db
import random

bp = Blueprint("index", __name__)

ALLOWED_EXTENSIONS = [".py"]


@bp.route("/", methods=["GET", "POST"])
def index():
    db = get_db()
    labs = db.execute("SELECT * FROM labs")

    # Okay, there's a bunch of SQL garbage we have to do, but let's cheat just this once.
    # Ideally, this should return the "most recent" lab.
    if request.method == "POST":

        file = request.files["fileupload"]

        # Check whether or not the user is logged in.
        user = getattr(g, "user", None)
        if user is None:
            print("No user found in this session. Redirecting...")
            return redirect(url_for("auth.login"))

        # If logged in, continue.
        else:
            if file.filename == "":
                print("Empty filename.")

            if file:
                filename = secure_filename(file.filename)

                # compile code

                # return result somehow

    return render_template("index.html", labs=labs)
