from flask import Blueprint, flash, redirect, render_template, request, session, url_for
from .db import get_db, query_db
import datetime

bp = Blueprint("labs", __name__, url_prefix="/labs")


def score(submitted, created):
    """Scoring function used to return a score based on the time difference
    between two dates. Takes two datetime strings as arguments, formatted in
    'HH:MM:SS, mm-dd-yy' format."""

    submitted = datetime.datetime.strptime(submitted, "%I:%M:%S%p, %m-%d-%y")
    created = datetime.datetime.strptime(created, "%I:%M:%S%p, %m-%d-%y")

    delta = (submitted - created).total_seconds()
    base_score = 100

    return int(base_score*(2 ** (-0.00004 * delta)))


@bp.route("/<int:lab_id>", methods=("GET", "POST"))
def labview(lab_id):
    """Lab view function responsible for handling submission requests."""

    # Retrieve lab and its corresponding list of solutions
    lab = query_db("SELECT * FROM labs WHERE id = ?", (lab_id,), True)
    solutions = query_db("SELECT * FROM submissions WHERE lab_id = ?", (lab["id"],))

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
            for solution in solutions:
                if solution["author_id"] == session["user_id"]:
                    already_submitted = True

            # If this is a brand new attempt, continue.
            if not already_submitted:

                # Retrieve current datetime as a string.
                now = datetime.datetime.now().strftime("%I:%M:%S%p, %m-%d-%y")
                created = lab["created"]

                # User's guess:
                output = request.form["output"]

                # Actual answer:
                correct_output = lab["output"]

                if output == correct_output:

                    # If the answer is correct, score the submission.
                    points = score(now, created)
                    flash("Yay! Looks like your output was correct! You got " + str(points) + " points.")

                    # add to their actual points (we do this in session so the user can see their own points increase)
                    session["points"] += points

                    # Queries to update points, submissions for the lab, and the number of solutions by the user and for the lab.
                    query_db("UPDATE users SET points = ? WHERE id = ?", (session["points"], session["user_id"]))
                    query_db("INSERT INTO submissions (author_id, author_username, lab_id, submitted) VALUES(?, ?, ?, ?)",
                             (session["user_id"], session["username"], lab["id"], now))

                    query_db("UPDATE users SET numsolutions = ? WHERE id = ?", (session["numsolutions"] + 1, session["user_id"]))
                    query_db("UPDATE labs SET numsolutions = ? WHERE id = ?", (lab["numsolutions"] + 1, lab["id"]))

                    get_db().commit()

                else:
                    flash("Incorrect output.")
            else:
                flash("You've already submitted a solution for this lab!")

    return render_template("lab.html",
                           title=lab["title"],
                           body=lab["body"],
                           date=lab["created"],
                           navbar=navbar,
                           solutions=solutions)

