from flask import Blueprint, render_template, session
from . import db

bp = Blueprint("leaderboard", __name__)


@bp.route("/leaderboard", methods=["GET"])
def leaderboard():

    navbar = render_template("default_navbar.html")

    # weird fix but ok
    # check if user is in session
    if "user_id" in session:
        navbar = render_template("user_navbar.html", username=session["username"], points=session["points"])

    users = db.get_entries("User", ["points"])

    return render_template("leaderboard.html", users=users, navbar=navbar)