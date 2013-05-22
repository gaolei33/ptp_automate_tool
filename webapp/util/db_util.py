import logging
import MySQLdb
from webapp import config
from webapp.exceptions import PTPDatabaseError

__author__ = 'Gao Lei'

_logger = logging.getLogger('default')


def exec_query(sql, db='MAIN'):
    query = sql
    return _exec_sql(query, db, 'QUERY')

def exec_cmds(sql, db='MAIN'):
    cmds = [cmd for cmd in sql.split('\n') if cmd]
    _exec_sql(cmds, db, 'CMDS')

def _exec_sql(exec_content, db, exec_type):
    conn = MySQLdb.connect(config.DB_INFO['HOST'], config.DB_INFO['USER'], config.DB_INFO['PASSWORD'], config.DB_INFO['NAMES'][db], config.DB_INFO['PORT'])
    try:
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
        raise PTPDatabaseError(err_msg)
    finally:
        if conn:
            conn.close()
    return result