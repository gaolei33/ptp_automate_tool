import logging
import MySQLdb
from webapp import config
from webapp.util import io_util

__author__ = 'Gao Lei'

_logger = logging.getLogger('default')


def get_connection():
    connection = MySQLdb.connect(config.DB_INFO['HOST'], config.DB_INFO['USER'], config.DB_INFO['PASSWORD'], config.DB_INFO['NAME'], config.DB_INFO['PORT'])
    return connection


def close_connection(connection):
    connection.close()


def exec_sql(sql):
    cmd = 'mysql -h %s -u %s -p%s %s -e "%s"' % (config.DB_INFO['HOST'], config.DB_INFO['USER'], config.DB_INFO['PASSWORD'], config.DB_INFO['NAME'], sql)
    error = io_util.exec_cmd(cmd)
    if error:
        err_msg = 'An error occurred while executing the SQL: %s, you\'d better restore development database before next steps.' % error
        _logger.error(err_msg)
        raise ValueError(err_msg)
    return error
