import sqlite3, click, os
from flask import current_app, g
from flask.cli import with_appcontext


# Weirdest and most nondescript module name EVER:
# g is the "global" (if that's what it stands for) cache in which all the
# information that might be accessed by a request is stored. If we need
# to access the database multiple times, g will be called on instead of
# a new connection being created.
def make_dicts(cursor, row):
    return dict((cursor.description[idx][0], value)
                for idx, value in enumerate(row))

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

        g.db.row_factory = make_dicts

    return g.db


def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv


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


@click.command("initdb")
@with_appcontext
def init_db_command():
    init_db()
    click.echo("Initialized the database.")



