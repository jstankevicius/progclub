# Script used to launch the application.
from progclub import create_app


def run():
    return create_app(test_config=None)

"""
if __name__ == "__main__":
    app = create_app(test_config=None)

    # We should probably disable debug
    app.run(debug=True)

    # Production:
    # app.run(host="0.0.0.0", debug=False)
"""