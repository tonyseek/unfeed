from flask import Blueprint, request
from werkzeug.contrib.atom import AtomFeed

from unfeed.models.site import Site
from unfeed.models.offline import OfflineIndex


bp = Blueprint('feed', __name__, url_prefix='/feed')


@bp.route('/<int:site_id>')
def atom(site_id):
    site = Site.query.get(site_id)
    indexes = OfflineIndex.query.filter_by(site_id=site.id) \
        .order_by(OfflineIndex.id.desc())

    feed = AtomFeed(site.name, feed_url=request.url, url=request.host_url)
    articles = (index.article for index in indexes[:50] if index.article)
    for article in articles:
        feed.add(
            article.title, article.content, content_type='html',
            author=article.author, url=article.url, id=article.item_id,
            updated=article.creation_time, published=article.published)
    return feed.get_response()
