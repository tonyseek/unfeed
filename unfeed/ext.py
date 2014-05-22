from flask.signals import Namespace
from flask.ext.sqlalchemy import SQLAlchemy
from raven.contrib.flask import Sentry


sentry = Sentry()
db = SQLAlchemy()
db_signals = Namespace()
db_created = db_signals.signal('created')
