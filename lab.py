from flask import Blueprint, flash, g, redirect, render_template, request, url_for
from werkzeug.exceptions import abort
from .auth import login_required
from .db import get_db

bp = Blueprint("lab", __name__)


@bp.route("/")
def index():
    db = get_db()
    # labs = db.execute("SELECT * FROM labs")

    # Okay, there's a bunch of SQL garbage we have to do, but let's cheat just this once.
    # Ideally, this should return the "most recent" lab.
    return render_template("index")