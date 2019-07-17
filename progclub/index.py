from flask import Blueprint, render_template, session
from . import db

bp = Blueprint("index", __name__)

@bp.route("/", methods=["GET"])
def index():
    labs = db.get_entries("Lab", ["-id"])

    navbar = render_template("default_navbar.html")

    # weird fix but ok
    # check if user is in session
    if "user_id" in session:
        navbar = render_template("user_navbar.html", username=session["username"], points=session["points"])

    return render_template("index.html",
                           labs=labs,
                           navbar=navbar)
