from flask import Blueprint, flash, redirect, render_template, request, session, url_for
from . import db
from datetime import datetime, timezone

bp = Blueprint("labs", __name__, url_prefix="/labs")


def score(submitted, created):
    """Scoring function used to return a score based on the time difference
    between two dates. Takes two datetime strings as arguments, formatted in
    'HH:MM:SS, mm-dd-yy' format."""
    delta = (submitted - created).total_seconds()
    base_score = 100

    return int(base_score*(2 ** (-0.00004 * delta)))


@bp.route("/<int:lab_id>", methods=("GET", "POST"))
def labview(lab_id):
    """Lab view function responsible for handling submission requests."""

    # Retrieve lab and its corresponding list of solutions
    lab = db.get_entry("Lab", lab_id)

    # Ugly
    submissions = [s for s in db.get_entries("Submission", ["submitted"]) if not (lab["name"] != s["lab_name"])]

    # Ugly
    navbar = render_template("default_navbar.html")

    # weird fix but ok
    if "user_id" in session:
        navbar = render_template("user_navbar.html", username=session["username"], points=session["points"])

    if request.method == "POST":

        # Check whether or not the user is logged in. If not, redirect to login page.
        # TODO: should probably make a login_required wrapper for this
        if "user_id" not in session:
            print("No user found in this session. Redirecting...")
            return redirect(url_for("auth.login"))

        # If logged in, continue.
        else:

            # Check if any solution in the lab's solution list has the user's ID attached to it.
            # TODO: can probably make this check much prettier
            already_submitted = False
            for solution in submissions:
                if solution["author_name"] == session["username"] and lab["name"] == solution["lab_name"]:
                    already_submitted = True

            # If this is a brand new attempt, continue.
            if not already_submitted:

                # Retrieve current datetime as a string.
                now = datetime.now(timezone.utc)
                created = lab["created"]
                output = request.form["output"]
                correct_output = lab["output"]

                if output == correct_output:

                    # If the answer is correct, score the submission.
                    points = score(now, created)
                    flash("Yay! Looks like your output was correct! You got " + str(points) + " points.")

                    # add to their actual points (we do this in session so the user can see their own points increase)
                    session["points"] += points
                    session["numsolutions"] += 1
                    username = session["username"]

                    # Queries to update points, submissions for the lab, and the number of solutions by the user and for the lab.
                    db.update_entry("User", username, {"points": session["points"], "numsolutions": session["numsolutions"]})
                    db.update_entry("Lab", lab_id, {"numsolutions": lab["numsolutions"] + 1})
                    db.entry("Submission", username + str(lab_id), {"lab_name": lab["name"], "author_name": session["username"], "submitted": now})

                else:
                    flash("Incorrect output.")
            else:
                flash("You've already submitted a solution for this lab!")

    return render_template("lab.html",
                           name=lab["name"],
                           body=lab["body"],
                           date=lab["created"],
                           navbar=navbar,
                           submissions=submissions)

