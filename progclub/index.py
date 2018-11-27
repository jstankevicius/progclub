from flask import Blueprint, flash, g, redirect, render_template, session
from .db import get_db
import random

bp = Blueprint("index", __name__)

ALLOWED_EXTENSIONS = [".py"]


@bp.route("/", methods=["GET"])
def index():
    db = get_db()

    labs = db.execute("SELECT * FROM labs")
    navbar = render_template("default_navbar.html")

    # weird fix but ok
    # fix later
    if "user_id" in session:
        navbar = render_template("user_navbar.html", username=session["username"])

    return render_template("index.html", labs=labs, navbar=navbar)
