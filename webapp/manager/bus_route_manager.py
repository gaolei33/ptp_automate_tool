import logging
import time
from webapp.manager import csv_manager, sql_manager, bus_stop_manager, bus_service_manager
from webapp.rule.bus_route_rule import BusRouteNCSRule, BusRouteLTARule
from webapp.util import db_util, string_util

__author__ = 'Gao Lei'

_logger = logging.getLogger('default')


def bus_route_add_or_update(csv_name, csv_type, bus_service_ids, sr_number):
    # retrieve data from CSV
    bus_routes, new_bus_service_ids = csv_manager.retrieve_multiple_data_from_csv(csv_name, csv_type, bus_service_ids)
    # incorrect bus service check
    if new_bus_service_ids:
        err_msg = 'Bus routes of %d bus services cannot be found in %s : %s' % (len(new_bus_service_ids), csv_name, ','.join(new_bus_service_ids))
        _logger.error(err_msg)
        raise ValueError(err_msg)

    # auto amend and complete bus route data
    rule = BusRouteNCSRule(bus_routes) if csv_type == 'BUS_ROUTE_NCS' else BusRouteLTARule(bus_routes)
    bus_routes_after_rules = rule.execute_rules()

    # new direction check
    directions = {(route[0], route[1]) for bus_route in bus_routes_after_rules for route in bus_route}
    new_directions = bus_service_manager.select_missing_directions(directions)
    if new_directions:
        new_directions_string = ','.join({'(%s,%s)' % (direction[0], direction[1]) for direction in new_directions})
        err_msg = '%d new directions need to be created : %s' % (len(new_directions), new_directions_string)
        _logger.error(err_msg)
        raise ValueError(err_msg)

    # new bus stops check
    bus_stop_ids = {route[3] for bus_route in bus_routes_after_rules for route in bus_route}
    new_bus_stop_ids = bus_stop_manager.select_bus_stops(bus_stop_ids)[1]
    if new_bus_stop_ids:
        err_msg = '%s new bus stops need to be created : %s' % (len(new_bus_stop_ids), ','.join(new_bus_stop_ids))
        _logger.error(err_msg)
        raise ValueError(err_msg)

    # wrap quotes for SQL generation
    bus_routes_wrap_quotes = string_util.wrap_quotes_except_null(bus_routes_after_rules)

    # generate SQL string
    sql = generate_sql(bus_routes_wrap_quotes, csv_type)

    # execute the generated SQL on development database
    db_util.exec_sql(sql)

    # save SQL string to file
    current_time = time.strftime('%Y%m%d%H%M%S')
    sql_name = 'SR_%s_%s_%s_%s.sql' % (sr_number, csv_type, '_'.join(bus_service_ids), current_time)
    sql_manager.save_sql(sql_name, sql)


def generate_sql(bus_routes, csv_type):
    sql = ''
    for bus_route in bus_routes:
        if csv_type == 'BUS_ROUTE_NCS':
            sql += "DELETE FROM bus_routes WHERE bus_service_id = %s AND provider = 'NCS';\n" % bus_route[0][0]
            for route in bus_route:
                sql += "INSERT INTO bus_routes (bus_service_id, direction, sequence, bus_stop_id, provider, express_code, distance, distance_fares_marker, weekday_first_trip, weekday_last_trip, saturday_first_trip, saturday_last_trip, sunday_first_trip, sunday_last_trip, note, shows_arrival_table, shows_fare_table, in_operation) VALUES (%s, %s, %s, %s, 'NCS', %s, %s, NULL, %s, %s, %s, %s, %s, %s, NULL, '0', '0', '1');\n" % (route[0], route[1], route[2], route[3], route[4], route[5], route[6], route[7], route[8], route[9], route[10], route[11])
        elif csv_type == 'BUS_ROUTE_LTA':
            sql += "DELETE FROM bus_routes WHERE bus_service_id = %s AND provider = 'LTA';\n" % bus_route[0][0]
            for route in bus_route:
                sql += "INSERT INTO bus_routes (bus_service_id, direction, sequence, bus_stop_id, provider, express_code, distance, distance_fares_marker, weekday_first_trip, weekday_last_trip, saturday_first_trip, saturday_last_trip, sunday_first_trip, sunday_last_trip, note, shows_arrival_table, shows_fare_table, in_operation) VALUES (%s, %s, %s, %s, 'LTA', %s, %s, %s, NULL, NULL, NULL, NULL, NULL, NULL, NULL, '0', '0', '1');\n" % (route[0], route[1], route[2], route[3], route[4], route[5], route[6])
    return sql