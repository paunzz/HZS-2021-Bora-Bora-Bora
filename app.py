from flask import Flask
from routes import dogadjaji
from base import session


# DATA_PATH = './static/'


def create_app(template_folder='templates', static_folder='static'):
    app = Flask("dogadjaji", template_folder=template_folder, static_folder=static_folder)

    @app.teardown_request
    def teardown_request(exception):
        if exception:
            session.rollback()
        else:
            session.commit()

    app.register_blueprint(dogadjaji)
    return app
