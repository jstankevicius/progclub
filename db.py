import sqlite3, click
from flask import current_app, g
from flask.cli import with_appcontext

# Weirdest and most nondescript module name EVER:
# g is the "global" (if that's what it stands for) cache in which all the
# information that might be accessed by a request is stored. If we need
# to access the database multiple times, g will be called on instead of
# a new connection being created.


def get_db():
    # We ensure that no database has been stored in g yet.
    if "db" not in g:
        g.db = sqlite3.connect(

            # Remember when we defined a databse in __init__.py? It's recalled here,
            # and we use the path stored in the DATABASE key to retrieve the location,
            # which, if everything executed correctly, should be the instance path
            # of the application.
            current_app.config["DATABASE"],
            detect_types=sqlite3.PARSE_DECLTYPES
        )

        # Thsi allows us to access the SQLite database like we would a dictionary, meaning
        # that we can access columns by name. Makes things very easy - if we want to get
        # a list of all users, we'd say something like db["users"].
        g.db.row_factory = sqlite3.Row

        return g.db


def close_db(e=None):
    db = g.pop("db", None)

    if db is not None:
        db.close()


def init_db():
    db = get_db()

    with current_app.open_resource("schema.sql") as f:
        db.executescript(f.read().decode("utf8"))


def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)


@click.command("init-db")
@with_appcontext
def init_db_command():
    init_db()
    click.echo("Initialized the database.")