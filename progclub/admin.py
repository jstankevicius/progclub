from subprocess import check_output
from flask import Blueprint, flash, g, redirect, render_template, request, session, url_for
from werkzeug.exceptions import abort
from werkzeug.utils import secure_filename
from .db import get_db, query_db

bp = Blueprint("admin", __name__)


def auth_admin():
    """Checks whether or not the user viewing the page is the admin. If they are,
    do nothing. If they're not, boot to index."""
    pass


@bp.route("/admin", methods=["GET", "POST"])
def admin_view():
    return render_template("admin.html")