import logging
from webapp.dao import bus_stop_dao
from webapp.exceptions import PTPValueError
from webapp.rule.bus_stop_rule import BusStopRule
from webapp.util import db_util, string_util
from webapp.manager import csv_manager, sql_manager

__author__ = 'Gao Lei'

_logger = logging.getLogger('default')


def get_bus_stops_from_csv(csv_name, bus_stop_ids):
    # retrieve data from CSV
    bus_stops, bus_stop_ids_missing = csv_manager.retrieve_multiple_data_from_csv(csv_name, 'BUS_STOP', bus_stop_ids)
    # raise exception if bus stop cannot be found in CSV
    if bus_stop_ids_missing:
        err_msg = '%d bus stops cannot be found in %s, please check whether you inputted incorrect bus stop IDs : %s' % (len(bus_stop_ids_missing), csv_name, ','.join(bus_stop_ids_missing))
        _logger.error(err_msg)
        raise PTPValueError(err_msg)
    # auto amend and complete bus stop data
    rule = BusStopRule(bus_stops)
    bus_stops_after_rules = rule.execute_rules()

    # retrieve data from DB
    bus_stop_ids_found_in_db = bus_stop_ids - bus_stop_dao.get_bus_stops_by_ids(bus_stop_ids)[1]
    # raise exception if bus stop already exist in DB
    if bus_stop_ids_found_in_db:
        err_msg = '%d bus stops already exist in DB, please use the Bus Stop Update function instead : %s' % (len(bus_stop_ids_found_in_db), ','.join(bus_stop_ids_found_in_db))
        _logger.error(err_msg)
        raise PTPValueError(err_msg)

    return bus_stops_after_rules


def get_bus_stops_from_db(bus_stop_ids):
    # retrieve data from DB
    bus_stops, bus_stop_ids_missing = bus_stop_dao.get_bus_stops_by_ids(bus_stop_ids)
    # raise exception if bus stop cannot be found in DB
    if bus_stop_ids_missing:
        err_msg = '%d bus stops cannot be found in DB, please check whether you inputted incorrect bus stop IDs : %s' % (len(bus_stop_ids_missing), ','.join(bus_stop_ids_missing))
        _logger.error(err_msg)
        raise PTPValueError(err_msg)

    return bus_stops


def bus_stop_add_or_update(bus_stops, sr_number, method):

    bus_stops_wrap_quotes = string_util.wrap_quotes_except_null(bus_stops)

    # generate SQL string
    sql = generate_sql(bus_stops_wrap_quotes, method)

    # execute the generated SQL on development database
    db_util.exec_cmds(sql)

    # save SQL string to file
    bus_stop_ids = [bus_stop_info[0] for bus_stop_info in bus_stops]
    sql_name = sql_manager.get_sql_name(sr_number, method, '_'.join(bus_stop_ids))
    sql_manager.save_sql(sql_name, sql)

    return sql_name


def generate_sql(bus_stops, method):
    sql = ''
    if method == 'BUS_STOP_ADD':
        for bus_stop in bus_stops:
            sql += "INSERT INTO bus_stops (id, linked_bus_stop_id, street_id, nearby_station_id, long_name, short_name, layout_num, max_pages, location_code, is_wab_accessible, is_non_bus_stop, is_interchange, is_pickup_point, has_arrival_info, has_arrival_panel, allows_boarding, allows_alighting, longitude, latitude) VALUES (%s, NULL, %s, NULL, %s, %s, %s, %s, %s, %s, %s, %s, '0', '0', '0', '1', '1', %s, %s);\n" % (bus_stop[0], bus_stop[1], bus_stop[2], bus_stop[3], bus_stop[4], bus_stop[5], bus_stop[6], bus_stop[7], bus_stop[8], bus_stop[9], bus_stop[10], bus_stop[11])
    else:
        for bus_stop in bus_stops:
            sql += "UPDATE bus_stops SET street_id = %s, long_name = %s, short_name = %s, layout_num = %s, max_pages = %s, location_code = %s, is_wab_accessible = %s, is_non_bus_stop = %s, is_interchange = %s, longitude= %s, latitude = %s WHERE id = %s;\n" % (bus_stop[1], bus_stop[2], bus_stop[3], bus_stop[4], bus_stop[5], bus_stop[6], bus_stop[7], bus_stop[8], bus_stop[9], bus_stop[10], bus_stop[11], bus_stop[0])
    return sql