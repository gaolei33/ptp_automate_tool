import logging
from webapp.dao import address_dao
from webapp.exceptions import PTPValueError
from webapp.manager import sql_manager
from webapp.rule.address_rule import AddressRule
from webapp.util import string_util, db_util

__author__ = 'Gao Lei'

_logger = logging.getLogger('default')


def postal_code_existing_check(postal_codes):
    postal_codes_in_db = address_dao.get_postal_codes_in_db(postal_codes)

    if postal_codes_in_db:
        err_msg = '%d postal codes already exist in DB, please input correctly : %s' % (len(postal_codes_in_db), ','.join(postal_codes_in_db))
        _logger.error(err_msg)
        raise PTPValueError(err_msg)


def address_add(addresses):

    rule = AddressRule(addresses)
    addresses_after_rules = rule.execute_rules()

    addresses_wrap_quotes = string_util.wrap_quotes_except_null(addresses_after_rules)

    # generate SQL string
    sql = generate_sql(addresses_wrap_quotes)

    # execute the generated SQL on development database
    db_util.exec_cmds(sql)

    # save SQL string to file
    postal_codes = [address[0] for address in addresses]
    sql_name = sql_manager.get_sql_name('None', 'ADDRESS_ADD', '_'.join(postal_codes))
    sql_manager.save_sql(sql_name, sql)

    return sql_name


def generate_sql(addresses):
    sql = 'SET @base_id_sequence = (SELECT MAX(id) FROM addresses);\n'
    for i, address in enumerate(addresses):
        sql += "INSERT INTO addresses (id, street_id, pnr_carpark_id, v3_address_id, block, building, postcode, longitude, latitude, date_modified) VALUES (@base_id_sequence + %d, %s, NULL, NULL, %s, NULL, %s, %s, %s, NOW());\n" % (i + 1, address[2], address[1], address[0], address[3], address[4])
    return sql

