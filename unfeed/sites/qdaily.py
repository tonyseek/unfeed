import copy

from brownant import Site, Dinergate
from brownant.pipeline import (TextResponseProperty, ElementTreeProperty,
                               XPathTextProperty)
from werkzeug.utils import cached_property
from lxml.html import tostring
from dateutil.parser import parse as parse_datetime

from .pipeline import DictionaryProperty, DictionaryValueProperty


site = Site('qdaily.com')


@site.route('qdaily.com', '/', defaults={'page': 1})
class QdailyIndex(Dinergate):

    URL_BASE = 'http://qdaily.com'
    URL_TEMPLATE = '{self.URL_BASE}/display/homes/articlemore?page={self.page}'

    text_response = TextResponseProperty()
    dict_response = DictionaryProperty()

    html_response = DictionaryValueProperty(dict_key='html')
    etree = ElementTreeProperty(text_response_attr='html_response')

    def __iter__(self):
        xpath_base = '//div[@class="article-container"]'
        xpath_hd = xpath_base + '//div[@class="content"]'
        xpath_bd = xpath_base + '//div[contains(@class, "hover-content")]'

        category = self.etree.xpath(
            xpath_hd + '//p[@class="category"]/a/text()')
        title = self.etree.xpath(xpath_bd + '//h2/a/text()')
        url = self.etree.xpath(xpath_bd + '//h2/a/@href')
        description = self.etree.xpath(
            xpath_bd + '//div[@class="excerpt"]/a/text()')

        return zip(category, title, url, description)


@site.route('qdaily.com', '/display/articles/<int:item_id>')
class QdailyArticle(Dinergate):

    URL_BASE = QdailyIndex.URL_BASE
    URL_TEMPLATE = '{self.URL_BASE}/display/articles/{self.item_id}'

    text_response = TextResponseProperty()
    etree = ElementTreeProperty()

    title = XPathTextProperty(xpath='//h2[@class="main-title"]/text()')
    subtitle = XPathTextProperty(xpath='//h4[@class="sub-title"]/text()')
    author = XPathTextProperty(
        xpath='//*[contains(@class, "author")]/span[@class="name"]/text()')
    content_etree = XPathTextProperty(
        xpath='//*[contains(@class, "article-detail")]/div[@class="bd"]',
        pick_mode='first')
    published_text = XPathTextProperty(
        xpath='//*[contains(@class, "author")]/span[@class="date"]/text()')

    @cached_property
    def content(self):
        content_etree = copy.deepcopy(self.content_etree)
        for node in content_etree.getiterator():
            for attr_name in ('href', 'src'):
                if attr_name not in node.attrib:
                    continue
                value = node.attrib[attr_name]
                if value.startswith('//'):
                    continue
                if not value.startswith('/'):
                    continue
                node.attrib[attr_name] = '/'.join([
                    self.URL_BASE, value.lstrip('/')])
        html = tostring(
            content_etree, pretty_print=True, encoding='unicode')
        return html.strip()

    @cached_property
    def published(self):
        return parse_datetime(self.published_text.strip())
