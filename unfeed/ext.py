from flask.signals import Namespace
from flask.ext.sqlalchemy import SQLAlchemy


db = SQLAlchemy()
db_signals = Namespace()
db_created = db_signals.signal('created')
