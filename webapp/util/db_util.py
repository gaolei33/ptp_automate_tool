import logging
import MySQLdb
from webapp import config

__author__ = 'Gao Lei'

_logger = logging.getLogger('default')


def exec_query(sql):
    query = sql
    return _exec_sql(query, 'QUERY')

def exec_cmds(sql):
    cmds = [cmd for cmd in sql.split('\n') if cmd]
    _exec_sql(cmds, 'CMDS')

def _exec_sql(exec_content, exec_type):
    conn = None
    try:
        conn = MySQLdb.connect(config.DB_INFO['HOST'], config.DB_INFO['USER'], config.DB_INFO['PASSWORD'], config.DB_INFO['NAME'], config.DB_INFO['PORT'])
        cur = conn.cursor()
        if exec_type == 'QUERY':
            cur.execute(exec_content)
            result = cur.fetchall()

        else:
            for cmd in exec_content:
                cur.execute(cmd)
            result = None
        cur.close()
        conn.commit()
    except Exception, ex:
        # rollback db if error occurred while executing SQLs
        if conn:
            conn.rollback()
        err_msg = 'An error occurred while executing SQL: %s, DB has been rollbacked.' % ex
        _logger.error(err_msg)
        raise ValueError(err_msg)
    finally:
        if conn:
            conn.close()
    return result