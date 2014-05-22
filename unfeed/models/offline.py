from flask import current_app

from unfeed.ext import db
from .base import EntityModel
from .site import Category


class OfflineIndex(EntityModel):
    """The offline index of sites."""

    __tablename__ = 'offline_index'

    category_id = db.Column(db.ForeignKey(Category.id), nullable=False)
    category = db.relationship(Category)
    title = db.Column(db.Unicode(60), nullable=False)
    relative_url = db.Column(db.Unicode(255), nullable=False)
    description = db.Column(db.UnicodeText, nullable=False)

    @classmethod
    def from_dinergate(cls, site, dinergate):
        for category_name, title, relative_url, description in dinergate:
            # strips spaces
            category_name = category_name.strip()
            title = title.strip()
            relative_url = relative_url.strip()
            description = description.strip()

            # checks for emtpy
            if any(not x for x in (category_name, title, relative_url,
                                   description)):
                continue

            # generates instance
            category = Category.get_or_create(name=category_name, site=site)
            instance = cls(
                category=category, title=title, relative_url=relative_url,
                description=description)

            # checks exists
            exists = cls.query.filter_by(
                relative_url=instance.relative_url).first()
            if exists:
                exists.category = category
                exists.title = title
                exists.description = description
                yield exists
            else:
                yield instance

    @property
    def site(self):
        return self.category.site

    @property
    def url(self):
        return '/'.join(self.site.url_base, relative_url.lstrip('/'))


def sync_indexes(site):
    dinergate = current_app.brownant.dispatch_url(site.start_url)
    indexes = OfflineIndex.from_dinergate(site, dinergate)
    db.session.add_all(list(indexes))
    db.session.commit()
