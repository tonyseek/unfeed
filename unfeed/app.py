from flask import Flask

from .ext import db
from .views.home import bp as home_bp


def create_app():
    app = Flask(__name__)

    app.config.from_pyfile('app.cfg')
    app.config.from_pyfile('dev.cfg', silent=True)
    app.config.from_pyfile('UNFEED_CONFIG', silent=True)

    db.init_app(app)

    app.register_blueprint(home_bp)

    return app
