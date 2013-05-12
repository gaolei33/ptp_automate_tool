import logging
import os
import time
from webapp import config
from webapp.exceptions import PTPValueError
from webapp.util import io_util

__author__ = 'Gao Lei'

_logger = logging.getLogger('default')


def save_sql(sql_name, sql):
    try:
        sql_path = os.path.join(config.SQL_FOLDER, sql_name)

        io_util.write_to_file(sql_path, sql)

        _logger.info('SQL file saved successfully: %s' % sql_path)
    except Exception, ex:
        err_msg = 'An error occurred while saving SQL to file: %s' % ex
        _logger.error(err_msg)
        raise PTPValueError(err_msg)


def get_sql(sql_name):
    sql_path = os.path.join(config.SQL_FOLDER, sql_name)

    if not os.path.exists(sql_path):
        err_msg = 'SQL file does not exist: %s' % sql_path
        _logger.error(err_msg)
        raise PTPValueError(err_msg)

    try:
        sql_file = file(sql_path)
    except Exception, ex:
        err_msg = 'An error occurred while reading SQL file: %s: %s' % (sql_path, ex)
        _logger.error(err_msg)
        raise PTPValueError(err_msg)

    return sql_file


def get_sql_name(sr_number, sql_type, other_info, ):
    current_time = time.strftime('%Y%m%d%H%M%S')
    sql_name = '[%s][%s]%s_%s.sql' % (sr_number, sql_type, other_info, current_time)
    return sql_name


def get_sql_list():
    sql_folder = config.SQL_FOLDER
    io_util.create_folder_if_not_exists(sql_folder)
    sql_list = [f for f in os.listdir(sql_folder) if os.path.isfile(os.path.join(sql_folder, f)) and f.lower().endswith('.sql')]
    # sort by date reversed
    sql_list.sort(key=lambda x: os.path.getmtime(os.path.join(sql_folder, x)), reverse=True)
    return sql_list


def delete(sql_name):
    sql_path = os.path.join(config.SQL_FOLDER, sql_name)
    io_util.delete_file(sql_path)