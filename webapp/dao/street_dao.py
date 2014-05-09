from webapp.util import db_util

__author__ = 'Gao Lei'


def get_first_matched_street_id_by_name(name):
    street_ids = get_street_by_keyword(name, 'NAME')
    street_id = street_ids[0][0] if street_ids else None
    return street_id


def get_street_by_keyword(keyword, keyword_type):
    if keyword_type == 'ID':
        sql = "select CONCAT(id), CONCAT(short_name), CONCAT(long_name) from streets where id like '%{0}%' limit 100".format(keyword)
    else:
        keyword = keyword.replace("'", "''")
        sql = "select CONCAT(id), CONCAT(short_name), CONCAT(long_name) from streets where short_name like '%{0}%' or long_name like '%{0}%' limit 100".format(keyword)
    result = db_util.exec_query(sql)
    return result