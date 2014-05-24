import copy


def eliminate_relative_urls(etree, base_url, attr_names=None,
                            without_side_effect=False):
    """Converts all relative URLs into absolute format in given element tree.

    This is useful while creating a feed (RSS or Atom) output.

    :param etree: the element tree object of lxml.
    :param base_url: the base url for creating absolute URLs.
    :param attr_names: optional. the names of scanning attrbiutes.
                       default: ['href', 'src']
    :param without_side_effect: optional. if be ``True``, the given element
                                tree will not be modified and a deepcopying
                                will be done for it.
                                default: ``False``
    """
    if attr_names is None:
        attr_names = ['href', 'src']
    if without_side_effect:
        etree = copy.deepcopy(etree)

    for node in etree.getiterator():
        for attr_name in attr_names:
            if attr_name not in node.attrib:
                continue
            value = node.attrib[attr_name]
            if value.startswith('//'):
                continue
            if not value.startswith('/'):
                continue
            node.attrib[attr_name] = '/'.join([base_url, value.lstrip('/')])

    return etree
