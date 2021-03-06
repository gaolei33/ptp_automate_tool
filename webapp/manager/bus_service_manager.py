import logging
from webapp.dao import bus_service_dao
from webapp.exceptions import PTPValueError
from webapp.manager import csv_manager, sql_manager
from webapp.rule.bus_service_rule import BusServiceRule
from webapp.util import db_util, string_util

__author__ = 'Gao Lei'

_logger = logging.getLogger('default')


def bus_service_add_or_update(csv_name, bus_service_ids, sr_number):
    # retrieve data from CSV
    bus_services, bus_service_ids_missing = csv_manager.retrieve_multiple_data_from_csv(csv_name, 'BUS_SERVICE', bus_service_ids)
    # incorrect bus service check
    if bus_service_ids_missing:
        err_msg = '%d bus services cannot be found in %s, please check whether you inputted incorrect bus service IDs : %s' % (len(bus_service_ids_missing), csv_name, ','.join(bus_service_ids_missing))
        _logger.error(err_msg)
        raise PTPValueError(err_msg)
    # auto amend and complete bus service data
    rule = BusServiceRule(bus_services)
    bus_services_after_rules = rule.execute_rules()

    # get operator name
    operator = get_operator_from_csv_name(csv_name)
    operator_wrap_quotes = "'%s'" % operator

    # wrap quotes for SQL generation
    bus_services_wrap_quotes = string_util.wrap_quotes_except_null(bus_services_after_rules)

    # generate SQL string
    sql = generate_sql_add_or_update(bus_services_wrap_quotes, operator_wrap_quotes)

    # execute the generated SQL on development database
    db_util.exec_cmds(sql)

    # save SQL string to file
    sql_name = sql_manager.get_sql_name(sr_number, 'BUS_SERVICE_ADD_OR_UPDATE', '_'.join(bus_service_ids))
    sql_manager.save_sql(sql_name, sql)

    return sql_name


def bus_service_enable_or_disable(bus_service_ids, enable_or_disable, sr_number):
    # find missing bus service ids
    bus_service_ids_missing = bus_service_dao.get_missing_bus_service_ids(bus_service_ids)
    # incorrect bus stop check
    if bus_service_ids_missing:
        err_msg = '%d bus services cannot be found in DB, please check whether you inputted incorrect bus service IDs : %s' % (len(bus_service_ids_missing), ','.join(bus_service_ids_missing))
        _logger.error(err_msg)
        raise PTPValueError(err_msg)

    # generate SQL string
    sql = generate_sql_enable_or_disable(bus_service_ids, enable_or_disable)

    # execute the generated SQL on development database
    db_util.exec_cmds(sql)

    # save SQL string to file
    sql_name = sql_manager.get_sql_name(sr_number, 'BUS_SERVICE_ENABLE_OR_DISABLE', '_'.join(bus_service_ids))
    sql_manager.save_sql(sql_name, sql)

    return sql_name


def get_operator_from_csv_name(csv_name):
    operator = ''
    OPERATOR_STRINGS = {'SMRT', 'SBST', 'TTS', 'GAS'}
    for operator_string in OPERATOR_STRINGS:
        if operator_string in csv_name.upper():
            operator = operator_string
            break
    if not operator:
        err_msg = 'Operator name cannot be found in the name of CSV file, please modify the name of the CSV file : %s' % (csv_name)
        _logger.error(err_msg)
        raise PTPValueError(err_msg)
    return operator


def generate_sql_add_or_update(bus_services, operator):
    sql = ''
    for bus_service in bus_services:
        sql += "DELETE FROM bus_service_directions WHERE bus_service_id = %s;\n" % bus_service[0][0]
        sql += "DELETE FROM bus_service_loops WHERE bus_service_id = %s;\n" % bus_service[0][0]
        sql += "DELETE FROM bus_services WHERE id = %s;\n" % bus_service[0][0]
        sql += "INSERT INTO bus_services(id, category, operator, uses_distance_fares, is_non_service_number, operating_hours_1, operating_hours_2, fare, contact, website) VALUES (%s, %s, %s, '1', '0', NULL, NULL, NULL, NULL, NULL);\n" % (bus_service[0][0], bus_service[0][2], operator)
        for direction in bus_service:
            sql += "INSERT INTO bus_service_directions(bus_service_id, direction, name, description, am_frequency_peak, am_frequency_off_peak, pm_frequency_peak, pm_frequency_off_peak) VALUES (%s, %s, NULL, NULL, %s, %s, %s, %s);\n" % (direction[0], direction[1], direction[3], direction[4], direction[5], direction[6])
        if bus_service[0][7] != 'NULL':
            sql += "INSERT INTO bus_service_loops(bus_service_id, loop_street_id) VALUES (%s, %s);\n" % (bus_service[0][0], bus_service[0][7])
    return sql


def generate_sql_enable_or_disable(bus_service_ids, enable_or_disable):
    sql = ''
    flag = '1' if enable_or_disable == 'BUS_SERVICE_ENABLE' else '0'
    bus_service_ids_string_wrap_quotes = ', '.join(["'%s'" % bus_service_id for bus_service_id in bus_service_ids])
    sql += "UPDATE bus_services SET uses_distance_fares = '%s' WHERE id IN (%s);\n" % (flag, bus_service_ids_string_wrap_quotes)
    sql += "UPDATE bus_routes SET in_operation = '%s' WHERE bus_service_id IN (%s);\n" % (flag, bus_service_ids_string_wrap_quotes)
    return sql