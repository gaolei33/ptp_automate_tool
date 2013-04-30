import logging
import re
import time
from webapp.rule.bus_stop_rule import BusStopRule
from webapp.util import db_util
from webapp.manager import csv_manager, sql_manager

__author__ = 'Gao Lei'

_logger = logging.getLogger('default')


def get_bus_stop_info(csv_name, bus_stop_ids):

    total_bus_stop_info = list()

    missing_bus_stop_ids = set()

    # retrieve data from CSV
    for bus_stop_id in bus_stop_ids:
        bus_stop_info = csv_manager.retrieve_data_from_csv(csv_name, 'BUS_STOP', bus_stop_id)

        if not bus_stop_info['DATA']:
            missing_bus_stop_ids.add(bus_stop_info['ID'])
        else:
            street_id = get_first_matched_street_id_from_name(bus_stop_info['DATA'][0][1])
            bus_stop_info['DATA'][0][1] = street_id

            total_bus_stop_info.append(bus_stop_info)

    # incorrect bus stop check
    if missing_bus_stop_ids:
        missing_bus_stop_idss_string = ','.join(missing_bus_stop_ids)
        err_msg = 'Bus stops (%s) cannot be found in %s' % (missing_bus_stop_idss_string, csv_name)
        _logger.error(err_msg)
        raise ValueError(err_msg)

    rule = BusStopRule(total_bus_stop_info)
    total_bus_stop_info_after_rules = rule.execute_rules()

    return total_bus_stop_info_after_rules


def bus_stop_update(total_bus_stop_info, csv_name, bus_stop_ids_string):

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
    sr_number = get_sr_number(csv_name)
    sql_name = 'SR_%s_BUS_STOP_%s_%s.sql' % (sr_number, bus_stop_ids_string, current_time)
    sql_manager.save_sql(sql_name, sql)


def get_first_matched_street_id_from_name(name):
    street_ids = street_search(name, 'NAME')
    street_id = street_ids[0][0] if street_ids else ''
    return street_id


def street_search(keyword, keyword_type):

    if keyword_type == 'ID':
        sql = "select id, short_name, long_name from streets where id like '%{0}%' limit 100".format(keyword)
    else:
        sql = "select id, short_name, long_name from streets where short_name like '%{0}%' or long_name like '%{0}%' limit 100".format(keyword)

    try:
        connection = db_util.get_connection()
        cursor = connection.cursor()
        cursor.execute(sql)
        result = cursor.fetchall()
        cursor.close()
        db_util.close_connection(connection)
    except Exception, ex:
        err_msg = 'An error occurred while searching street: %s' % ex
        _logger.error(err_msg)
        raise ValueError(err_msg)

    return result


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
        sql += "INSERT INTO bus_stops (id, linked_bus_stop_id, street_id, nearby_station_id, long_name, short_name, location_code, is_wab_accessible, is_non_bus_stop, is_interchange, is_pickup_point, has_arrival_info, has_arrival_panel, allows_boarding, allows_alighting, longitude, latitude) VALUES(%s, NULL, %s, NULL, %s, %s, %s, %s, %s, '0', '0', '0', '0', '1', '1', '', '');\n" % (bus_stop_info[0], bus_stop_info[1], bus_stop_info[2], bus_stop_info[3], bus_stop_info[4], bus_stop_info[5], bus_stop_info[6])
    return sql


def get_sr_number(csv_name):
    m = re.search(r'^SR_(\d+)_', csv_name)
    if m:
        sr_number = m.group(1)
    else:
        sr_number = 'Unknown'
    return sr_number