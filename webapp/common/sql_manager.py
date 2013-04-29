import logging
import os
from webapp import config
from webapp.common import io_utils

__author__ = 'Gao Lei'

_logger = logging.getLogger('default')

def save_sql(sql_name, sql):

    try:
        sql_folder = config.SQL_FOLDER
        sql_path = os.path.join(sql_folder, sql_name)

        io_utils.write_to_file(sql_path, sql)

        _logger.info('SQL file saved successfully: %s' % sql_path)
    except Exception, ex:
        err_msg = 'An error occurred while saving SQL to file: %s' % ex
        _logger.error(err_msg)
        raise ValueError(err_msg)

def get_sql(sql_name):

    sql_folder = config.SQL_FOLDER
    sql_path = os.path.join(sql_folder, sql_name)

    if not os.path.exists(sql_path):
        err_msg = 'SQL file does not exist: %s' % sql_path
        _logger.error(err_msg)
        raise ValueError(err_msg)

    try:
        sql_file = file(sql_path)
    except Exception, ex:
        err_msg = 'An error occurred while reading SQL file: %s: %s' % (sql_path, ex)
        _logger.error(err_msg)
        raise ValueError(err_msg)

    return sql_file