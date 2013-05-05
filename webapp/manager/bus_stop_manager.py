import logging
import time
from webapp.rule.bus_stop_rule import BusStopRule
from webapp.util import db_util, string_util
from webapp.manager import csv_manager, sql_manager

__author__ = 'Gao Lei'

_logger = logging.getLogger('default')


def get_bus_stops_from_csv(csv_name, bus_stop_ids):
    # retrieve data from CSV
    bus_stops, bus_stop_ids_missing = csv_manager.retrieve_multiple_data_from_csv(csv_name, 'BUS_STOP', bus_stop_ids)
    # incorrect bus stop check
    if bus_stop_ids_missing:
        err_msg = '%d bus stops cannot be found in %s : %s' % (len(bus_stop_ids_missing), csv_name, ','.join(bus_stop_ids_missing))
        _logger.error(err_msg)
        raise ValueError(err_msg)
    # auto amend and complete bus stop data
    rule = BusStopRule(bus_stops)
    bus_stops_after_rules = rule.execute_rules()

    return bus_stops_after_rules


def get_bus_stops_from_db(bus_stop_ids):
    # retrieve data from DB
    bus_stops, bus_stop_ids_missing = select_bus_stops(bus_stop_ids)
    # incorrect bus stop check
    if bus_stop_ids_missing:
        err_msg = '%d bus stops cannot be found in DB : %s' % (len(bus_stop_ids_missing), ','.join(bus_stop_ids_missing))
        _logger.error(err_msg)
        raise ValueError(err_msg)

    return bus_stops


def bus_stop_add_or_update(bus_stops, sr_number, method):

    bus_stops_wrap_quotes = string_util.wrap_quotes_except_null(bus_stops)

    # generate SQL string
    sql = generate_sql(bus_stops_wrap_quotes, method)

    # execute the generated SQL on development database
    db_util.exec_sql(sql)

    # save SQL string to file
    bus_stop_ids = [bus_stop_info[0] for bus_stop_info in bus_stops]
    current_time = time.strftime('%Y%m%d%H%M%S')
    sql_name = 'SR_%s_%s_%s_%s.sql' % (sr_number, method, '_'.join(bus_stop_ids), current_time)
    sql_manager.save_sql(sql_name, sql)


def generate_sql(bus_stops, method):
    sql = ''
    if method == 'BUS_STOP_ADD':
        for bus_stop in bus_stops:
            sql += "DELETE FROM bus_stops WHERE id = %s;\n" % bus_stop[0]
            sql += "INSERT INTO bus_stops (id, linked_bus_stop_id, street_id, nearby_station_id, long_name, short_name, location_code, is_wab_accessible, is_non_bus_stop, is_interchange, is_pickup_point, has_arrival_info, has_arrival_panel, allows_boarding, allows_alighting, longitude, latitude) VALUES (%s, NULL, %s, NULL, %s, %s, %s, %s, %s, %s, '0', '0', '0', '1', '1', '', '');\n" % (bus_stop[0], bus_stop[1], bus_stop[2], bus_stop[3], bus_stop[4], bus_stop[5], bus_stop[6], bus_stop[7])
    else:
        for bus_stop in bus_stops:
            sql += "UPDATE bus_stops SET street_id = %s, long_name = %s, short_name = %s, location_code = %s, is_wab_accessible = %s, is_non_bus_stop = %s, is_interchange = %s WHERE id = %s;\n" % (bus_stop[1], bus_stop[2], bus_stop[3], bus_stop[4], bus_stop[5], bus_stop[6], bus_stop[7], bus_stop[0])
    return sql


def select_bus_stops(bus_stop_ids):

    try:
        bus_stop_ids_string_wrap_quotes = ', '.join({"'%s'" % bus_stop_id for bus_stop_id in bus_stop_ids})

        connection = db_util.get_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT CONCAT(id), CONCAT(street_id), CONCAT(long_name), CONCAT(short_name), IF(location_code IS NULL, '', CONCAT(location_code)), CONCAT(is_wab_accessible), CONCAT(is_non_bus_stop), CONCAT(is_interchange) FROM bus_stops WHERE id IN (%s);" % bus_stop_ids_string_wrap_quotes)
        result = cursor.fetchall()

        bus_stop_ids_found = {bus_stop[0] for bus_stop in result}
        bus_stop_ids_missing = bus_stop_ids - bus_stop_ids_found

        cursor.close()
        db_util.close_connection(connection)
    except Exception, ex:
        err_msg = 'An error occurred while select bus stops from DB: %s' % ex
        _logger.error(err_msg)
        raise ValueError(err_msg)

    return result, bus_stop_ids_missing