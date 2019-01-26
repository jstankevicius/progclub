from flask import Blueprint, redirect, render_template, request, session, url_for
from . import db
from datetime import datetime, timezone


bp = Blueprint("admin", __name__)


# horribly insecure
# just like me
@bp.route("/admin", methods=["GET", "POST"])
def admin_view():
    # literally just redirect to index if
    #   a. the user is not logged in
    #   b. if logged in, the user is not me

    if request.method == "POST":
        name = request.form["name"]
        body = request.form["body"]
        output = request.form["output"]
        now = datetime.now(timezone.utc)
        print(now)
        key = int(now.strftime("%y%m%d%I%M%S"))
        db.entry("Lab", key,
                 {"name": name, "body": body, "output": output, "numsolutions": 0, "created": now, "id": key})

        return redirect(url_for("index"))

    # oh god why
    if request.method == "GET":
        if "username" in session:
            if session["username"] == "test_user":
                print("Redirecting to admin page.")
                return render_template("admin.html")
            else:
                print("User logged in, but is not admin user.")
                return redirect(url_for("index"))
        else:
            print("User not logged in.")
            return redirect(url_for("index"))


