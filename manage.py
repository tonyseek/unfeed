#!/usr/bin/env python

from flask.ext.script import Manager
from unfeed.app import create_app
from unfeed.ext import db, db_created


app = create_app()
manager = Manager(app)


@manager.shell
def context():
    return {'app': app, 'db': db}


@manager.command
def syncdb(destory=False, verbose=False):
    """Creates database."""
    import unfeed.models  # noqa

    db.engine.echo = bool(verbose)
    if destory:
        db.drop_all()
    db.create_all()
    db_created.send(db)


if __name__ == '__main__':
    manager.run()
