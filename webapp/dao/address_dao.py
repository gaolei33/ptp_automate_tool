from webapp.util import db_util

__author__ = 'Gao Lei'


def get_postal_codes_in_db(postal_codes):
    postal_codes_string_wrap_quotes = ', '.join(["'%s'" % postal_code for postal_code in postal_codes])
    sql = 'SELECT CONCAT(postcode) FROM addresses WHERE postcode IN (%s);' % postal_codes_string_wrap_quotes

    result = db_util.exec_query(sql)

    postal_codes_in_db = {address[0] for address in result}

    return postal_codes_in_db