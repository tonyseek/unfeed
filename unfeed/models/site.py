from werkzeug.urls import url_parse
from werkzeug.utils import import_string, cached_property

from unfeed.ext import db, db_created
from .base import EntityModel


class Site(EntityModel):
    """The third-part site."""

    __tablename__ = 'site'

    name = db.Column(db.Unicode(20), nullable=False)
    start_url = db.Column(db.Unicode(255), nullable=False)
    dinergate_name = db.Column(db.Unicode(30), nullable=False)

    @db.validates('start_url')
    def validate_start_url(self, key, value):
        url = url_parse(value)
        if url.scheme not in ('http', 'https') or not url.netloc:
            raise ValueError(value)
        return url.to_url()

    @cached_property
    def dinergate_class(self):
        return import_string('unfeed.sites.' + self.dinergate_name)

    @cached_property
    def url_base(self):
        return self.dinergate_class.URL_BASE


class Category(EntityModel):
    """The category of third-part site."""

    __tablename__ = 'category'

    name = db.Column(db.Unicode(20), nullable=False)
    site_id = db.Column(db.ForeignKey('site.id'), nullable=False)
    site = db.relationship(Site)


@db_created.connect_via(db)
def initial_sites(sender):
    sites = [
        Site(name='好奇心日报', start_url='http://qdaily.com/',
             dinergate_name='qdaily:QdailyIndex'),
    ]
    db.session.add_all(sites)
    db.session.commit()
