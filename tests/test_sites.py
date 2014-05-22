from pytest import fixture


start_urls = [
    'http://qdaily.com/',
]


def test_index(app):
    for start_url in start_urls:
        index = app.brownant.dispatch_url(start_url)
        index_list = list(index)
        assert set(index_list) == set(index)
        assert len(index_list) == len(set(index))
        assert len(index_list) > 0
