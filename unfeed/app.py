from flask import Flask
from brownant import Brownant
from werkzeug.utils import import_string

from .ext import db


blueprints = [
    'home',
]

brownant_sites = [
    'qdaily',
]


def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('app.cfg')
    app.config.from_pyfile('dev.cfg', silent=True)
    app.config.from_pyfile('UNFEED_CONFIG', silent=True)

    # extensions
    db.init_app(app)

    # blueprints
    for bp in blueprints:
        import_name = '%s.views.%s:bp' % (__package__, bp)
        app.register_blueprint(import_string(import_name))

    # brownant
    app.brownant = Brownant()
    for site in brownant_sites:
        import_name = '%s.sites.%s:site' % (__package__, site)
        app.brownant.mount_site(import_name)

    return app
