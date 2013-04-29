import MySQLdb
from webapp import config
from webapp.common import io_utils

__author__ = 'Gao Lei'

def get_connection():

    connection = MySQLdb.connect(config.DB_INFO['HOST'], config.DB_INFO['USER'], config.DB_INFO['PASSWORD'], config.DB_INFO['NAME'], config.DB_INFO['PORT'])

    return connection


def close_connection(connection):

    connection.close()


def exec_sql(sql):

    cmd = 'mysql -h %s -u %s -p%s %s -e "%s"' % (config.DB_INFO['HOST'], config.DB_INFO['USER'], config.DB_INFO['PASSWORD'], config.DB_INFO['NAME'], sql)
    error = io_utils.exec_cmd(cmd)

    return error
