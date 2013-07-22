import logging
from webapp.dao import street_dao

__author__ = 'Gao Lei'

_logger = logging.getLogger('default')


def street_search(keyword, keyword_type):
    return street_dao.get_street_by_keyword(keyword, keyword_type)