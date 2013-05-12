import logging
from webapp.exceptions import PTPValueError

__author__ = 'Gao Lei'

_logger = logging.getLogger('default')


def wrap_quotes_except_null(origin_obj):
    if type(origin_obj) in (str, unicode):
        origin_obj = origin_obj.replace("'", "''")
        target_obj = origin_obj if origin_obj == 'NULL' else "'%s'" % origin_obj
    else:
        try:
            target_obj = [wrap_quotes_except_null(item) for item in origin_obj]
        except:
            err_msg = 'An error occurred while wrapping quotes for SQL generation: data must be strings.'
            _logger.error(err_msg)
            raise PTPValueError(err_msg)
    return target_obj