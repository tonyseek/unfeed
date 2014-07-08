from flask import current_app

from unfeed.ext import db
from .base import EntityModel
from .site import Category, Site


class OfflineIndex(EntityModel):
    """The offline index of sites."""

    __tablename__ = 'offline_index'

    category_id = db.Column(db.ForeignKey(Category.id), nullable=False)
    category = db.relationship(Category)
    site_id = db.Column(db.ForeignKey(Site.id), nullable=False)
    title = db.Column(db.Unicode(60), nullable=False)
    relative_url = db.Column(db.Unicode(255), nullable=False, unique=True)
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

            # checks exists
            instance = cls.query.filter_by(relative_url=relative_url).first()
            if not instance:
                instance = cls(relative_url=relative_url)
            instance.category = category
            instance.title = title
            instance.description = description
            instance.site_id = site.id
            yield instance

    @property
    def site(self):
        return self.category.site

    @property
    def url(self):
        return '/'.join([self.site.url_base, self.relative_url.lstrip('/')])


class OfflineArticle(EntityModel):

    __tablename__ = 'offline_article'

    title = db.Column(db.Unicode(60), nullable=False)
    content = db.Column(db.UnicodeText, nullable=False)
    published = db.Column(db.DateTime, nullable=False)
    related_index_id = db.Column(
        db.ForeignKey(OfflineIndex.id), nullable=False)
    related_index = db.relationship(
        OfflineIndex, backref=db.backref('article', uselist=False))
    subtitle = db.Column(db.Unicode(60))
    author = db.Column(db.Unicode(60))
    site_id = db.Column(db.ForeignKey(Site.id), nullable=False)
    item_id = db.Column(db.Unicode(60))

    def __repr__(self):
        return super(OfflineArticle, self).__repr__(
            skip_attrs={'related_index'})

    @property
    def url(self):
        return self.related_index.url

    @classmethod
    def from_dinergate(cls, index, dinergate):
        site_id = index.site.id
        item_id = dinergate.item_id

        instance = cls.query.filter_by(
            site_id=site_id, item_id=item_id).first()
        if not instance:
            instance = cls(
                site_id=site_id, item_id=item_id, related_index=index)

        instance.title = dinergate.title
        instance.subtitle = dinergate.subtitle
        instance.author = dinergate.author
        instance.content = dinergate.content
        instance.published = dinergate.published

        return instance


def sync_indexes(site):
    dinergate = current_app.brownant.dispatch_url(site.start_url)
    indexes = OfflineIndex.from_dinergate(site, dinergate)
    indexes = list(indexes)
    db.session.add_all(indexes)
    db.session.commit()
    return indexes


def sync_articles(indexes):
    dispatch_url = current_app.brownant.dispatch_url
    articles = [
        OfflineArticle.from_dinergate(index, dinergate=dispatch_url(index.url))
        for index in indexes]
    db.session.add_all(articles)
    db.session.commit()
    return articles
