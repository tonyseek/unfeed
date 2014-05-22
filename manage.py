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


@manager.command
def fetch():
    """Fetches to offline."""
    from unfeed.models import Site, sync_indexes, sync_articles
    for site in Site.query:
        indexes = sync_indexes(site)
        articles = sync_articles(indexes)
        for article in articles:
            print('%s: %s: %s: %s' % (
                article.title, article.item_id, article.author,
                article.published))
        print('== %d articles in %s' % (len(articles), site.name))


if __name__ == '__main__':
    manager.run()
