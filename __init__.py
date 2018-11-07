import os
from flask import Flask
from . import db


def create_app(test_config=None):
    # test_config is an application configuration that makes launching easy. It's populated with values
    # that make things convenient, and should never be deployed. We pass it in during testing.

    app = Flask(__name__, instance_relative_config=True)

    # SECRET_KEY is set to a convenient value for testing. This should be changed once we actually deploy.
    # DATABASE is the path of our SQLite (or other) database.
    app.config.from_mapping(SECRET_KEY="dev", DATABASE=os.path.join(app.instance_path, "app.sqlite"))

    if test_config is None:
        # If there is a configured instance, we load that instead, if we are not testing. config.py
        # can be used to store real values that we don't want to be visible, like a real SECRET_KEY.
        app.config.from_pyfile("config.py", silent=True)
    else:
        # Otherwise, we load a test configuration to make stuff easier for ourselves.
        app.config.from_mapping(test_config)

    # We ensure that the application instance path exists. If it does, we simply ignore the error,
    # as everything is going as expected.
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    db.init_app(app)


    # a simple page that says hello
    @app.route('/hello')
    def hello():
        return 'Hello, World!'

    return app

