import MySQLdb
from webapp import config

__author__ = 'Gao Lei'

def get_connection():

    connection = MySQLdb.connect(config.DB_INFO['HOST'], config.DB_INFO['USER'], config.DB_INFO['PASSWORD'], config.DB_INFO['NAME'], config.DB_INFO['PORT'])

    return connection

def close_connection(connection):

    connection.close()