from flask import Blueprint, render_template, session
from .db import get_db, query_db

bp = Blueprint("index", __name__)


@bp.route("/", methods=["GET"])
def index():
    db = get_db()

    labs = query_db("SELECT * FROM labs ORDER BY id DESC")
    solutions = query_db("SELECT * FROM submissions")

    navbar = render_template("default_navbar.html")

    # weird fix but ok
    # check if user is in session
    if "user_id" in session:
        navbar = render_template("user_navbar.html", username=session["username"], points=session["points"])

    return render_template("index.html",
                           labs=labs,
                           solutions=solutions,
                           navbar=navbar)
