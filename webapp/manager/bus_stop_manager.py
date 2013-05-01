import logging
import time
from webapp.rule.bus_stop_rule import BusStopRule
from webapp.util import db_util
from webapp.manager import csv_manager, sql_manager

__author__ = 'Gao Lei'

_logger = logging.getLogger('default')


def get_bus_stop_info_from_csv(csv_name, bus_stop_ids):
    # retrieve data from CSV
    total_bus_stop_info, missing_bus_stop_ids = csv_manager.retrieve_multiple_data_from_csv(csv_name, 'BUS_STOP', bus_stop_ids)
    # incorrect bus stop check
    if missing_bus_stop_ids:
        err_msg = '%d bus stops cannot be found in %s : %s' % (len(missing_bus_stop_ids), csv_name, ','.join(missing_bus_stop_ids))
        _logger.error(err_msg)
        raise ValueError(err_msg)

    rule = BusStopRule(total_bus_stop_info)
    total_bus_stop_info_after_rules = rule.execute_rules()

    return total_bus_stop_info_after_rules


def get_bus_stop_info_from_db(bus_stop_ids):
    # retrieve data from DB
    total_bus_stop_info, bus_stop_ids_missing = select_bus_stops(bus_stop_ids)
    # incorrect bus stop check
    if bus_stop_ids_missing:
        bus_stop_ids_missing_string = ','.join(bus_stop_ids_missing)
        err_msg = '%d bus stops cannot be found in DB : %s' % (len(bus_stop_ids_missing), bus_stop_ids_missing_string)
        _logger.error(err_msg)
        raise ValueError(err_msg)

    return total_bus_stop_info


def bus_stop_update(total_bus_stop_info, sr_number, bus_stop_ids_string):

    total_bus_stop_info_wrap_quotes = wrap_quotes(total_bus_stop_info)

    sql = generate_sql(total_bus_stop_info_wrap_quotes)

    # execute the generated SQL on development database
    error = db_util.exec_sql(sql)
    if error:
        err_msg = 'An error occurred while executing the SQL: %s, you\'d better restore development database before next steps.' % error
        _logger.error(err_msg)
        raise ValueError(err_msg)

    # save SQL string to file
    current_time = time.strftime('%Y%m%d%H%M%S')
    sql_name = 'SR_%s_BUS_STOP_%s_%s.sql' % (sr_number, bus_stop_ids_string, current_time)
    sql_manager.save_sql(sql_name, sql)


def wrap_quotes(origin_total_bus_stop_info):
    target_total_bus_stop_info = []
    for origin_bus_stop_info in origin_total_bus_stop_info:
        target_bus_stop_info = []
        for origin_col in origin_bus_stop_info:
            if origin_col == 'NULL':
                target_col = origin_col
            else:
                target_col = "'%s'" % origin_col
            target_bus_stop_info.append(target_col)
        target_total_bus_stop_info.append(target_bus_stop_info)
    return target_total_bus_stop_info


def generate_sql(total_bus_stop_info):
    sql = ''
    for bus_stop_info in total_bus_stop_info:
        sql += "DELETE FROM bus_stops WHERE id = %s;\n" % bus_stop_info[0]
        sql += "INSERT INTO bus_stops (id, linked_bus_stop_id, street_id, nearby_station_id, long_name, short_name, location_code, is_wab_accessible, is_non_bus_stop, is_interchange, is_pickup_point, has_arrival_info, has_arrival_panel, allows_boarding, allows_alighting, longitude, latitude) VALUES (%s, NULL, %s, NULL, %s, %s, %s, %s, %s, %s, '0', '0', '0', '1', '1', '', '');\n" % (bus_stop_info[0], bus_stop_info[1], bus_stop_info[2], bus_stop_info[3], bus_stop_info[4], bus_stop_info[5], bus_stop_info[6], bus_stop_info[7])
    return sql


def select_bus_stops(bus_stop_ids):

    try:
        bus_stop_ids_string_wrap_quotes = ', '.join({"'%s'" % bus_stop_id for bus_stop_id in bus_stop_ids})

        connection = db_util.get_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT id, street_id, long_name, short_name, IF(location_code IS NULL, '', location_code), is_wab_accessible, is_non_bus_stop, is_interchange FROM bus_stops WHERE id IN (%s);" % bus_stop_ids_string_wrap_quotes)
        result = cursor.fetchall()

        bus_stop_ids_found = {bus_stop_info[0] for bus_stop_info in result}
        bus_stop_ids_missing = bus_stop_ids - bus_stop_ids_found

        cursor.close()
        db_util.close_connection(connection)
    except Exception, ex:
        err_msg = 'An error occurred while select bus stops from DB: %s' % ex
        _logger.error(err_msg)
        raise ValueError(err_msg)

    return result, bus_stop_ids_missing