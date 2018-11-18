import functools
from flask import Blueprint, flash, g, redirect, render_template, request, session, url_for
from werkzeug.security import check_password_hash, generate_password_hash
from .db import get_db, query_db

bp = Blueprint("labs", __name__, url_prefix="/labs")


@bp.route("/<int:id>", methods=("GET", "POST"))
def lab(id):
    if request.method == "POST":
        pass

    lab = query_db("select * from labs where id = ?", (id,))[0]

    return render_template("lab.html", title=lab["title"], body=lab["body"])

