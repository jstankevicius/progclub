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
    return render_template("index.html", labs=labs)
