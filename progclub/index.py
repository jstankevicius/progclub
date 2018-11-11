from flask import Blueprint, flash, g, redirect, render_template, request, url_for
from werkzeug.exceptions import abort
from werkzeug.utils import secure_filename
from .auth import login_required
from .db import get_db

bp = Blueprint("index", __name__)

ALLOWED_EXTENSIONS = [".py"]


@bp.route("/", methods=["GET", "POST"])
def index():
    db = get_db()
    # labs = db.execute("SELECT * FROM labs")

    # Okay, there's a bunch of SQL garbage we have to do, but let's cheat just this once.
    # Ideally, this should return the "most recent" lab.
    if request.method == "POST":

        @login_required
        def upload_file():
            if "file" not in request.files:
                return redirect(request.url)

            file = request.files["file"]

            if file.filename == "":
                return redirect(request.url)

            if file:
                filename = secure_filename(file.filename)
                print(filename)
                # compile code

                # return result somehow

        upload_file()

    return render_template("index.html")
