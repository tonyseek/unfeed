from brownant import Site, Dinergate
from brownant.pipeline import TextResponseProperty, ElementTreeProperty
from werkzeug.utils import cached_property

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
