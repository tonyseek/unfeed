from flask import Blueprint, render_template, redirect, url_for

from unfeed.models.site import Site
from unfeed.models.offline import OfflineIndex, OfflineArticle


bp = Blueprint('home', __name__)


@bp.route('/')
def home():
    sites = Site.query.all()
    return render_template('home.html', sites=sites)


@bp.route('/site/<int:site_id>')
def site(site_id):
    site = Site.query.get_or_404(site_id)
    indexes = OfflineIndex.query \
        .filter_by(site_id=site.id) \
        .order_by(OfflineIndex.id.desc()) \
        .all()
    return render_template('site.html', site=site, indexes=indexes)


@bp.route('/site/<int:site_id>/article/<int:article_id>')
def article(site_id, article_id):
    site = Site.query.get(site_id)
    article = OfflineArticle.query.get_or_404(article_id)

    if not site or article.site_id != site.id:
        stricted_url = url_for(
            '.article', site_id=article.site_id, article_id=article.id)
        return redirect(stricted_url)

    return render_template('article.html', site=site, article=article)
