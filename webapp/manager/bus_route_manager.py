import logging
from webapp.dao import bus_stop_dao
from webapp.dao import bus_service_dao
from webapp.exceptions import PTPValueError
from webapp.manager import csv_manager, sql_manager
from webapp.rule.bus_route_rule import BusRouteNCSRule, BusRouteLTARule
from webapp.util import db_util, string_util

__author__ = 'Gao Lei'

_logger = logging.getLogger('default')


def bus_route_add_or_update(csv_name_ncs, csv_name_lta, bus_service_ids, sr_number):
    # retrieve bus route data and perform some validations
    bus_routes_ncs = retrieve_bus_routes(csv_name_ncs, 'BUS_ROUTE_NCS', bus_service_ids)
    bus_routes_lta = retrieve_bus_routes(csv_name_lta, 'BUS_ROUTE_LTA', bus_service_ids)

    # bus route sequence check between NCS and LTA sets
    sequence_check_between_ncs_and_lta(bus_routes_ncs, bus_routes_lta)

    # wrap quotes for SQL generation
    bus_routes_ncs_wrap_quotes = string_util.wrap_quotes_except_null(bus_routes_ncs)
    bus_routes_lta_wrap_quotes = string_util.wrap_quotes_except_null(bus_routes_lta)

    # generate SQL string
    sql = generate_sql(bus_routes_ncs_wrap_quotes, bus_routes_lta_wrap_quotes)

    # execute the generated SQL on development database
    db_util.exec_cmds(sql)

    # save SQL string to file
    sql_name = sql_manager.get_sql_name(sr_number, 'BUS_ROUTE', '_'.join(bus_service_ids))
    sql_manager.save_sql(sql_name, sql)

    return sql_name


def retrieve_bus_routes(csv_name, method, bus_service_ids):
    # retrieve data from CSV
    bus_routes, new_bus_service_ids = csv_manager.retrieve_multiple_data_from_csv(csv_name, method, bus_service_ids)
    # incorrect bus service check
    if new_bus_service_ids:
        err_msg = 'Bus routes of %d bus services cannot be found in %s, please check whether you inputted incorrect bus service IDs : %s' % (len(new_bus_service_ids), csv_name, ','.join(new_bus_service_ids))
        _logger.error(err_msg)
        raise PTPValueError(err_msg)

    # auto amend and complete bus route data
    rule = BusRouteNCSRule(bus_routes) if method == 'BUS_ROUTE_NCS' else BusRouteLTARule(bus_routes)
    bus_routes_after_rules = rule.execute_rules()

    # new direction check
    directions = {(route[0], route[1]) for bus_route in bus_routes_after_rules for route in bus_route}
    new_directions = bus_service_dao.get_missing_directions(directions)
    if new_directions:
        new_directions_string = ','.join({'(%s,%s)' % (direction[0], direction[1]) for direction in new_directions})
        err_msg = '%d new directions need to be created, please use the Bus Service Add / Update function first : %s' % (len(new_directions), new_directions_string)
        _logger.error(err_msg)
        raise PTPValueError(err_msg)

    # new bus stops check
    bus_stop_ids = {route[3] for bus_route in bus_routes_after_rules for route in bus_route}
    new_bus_stop_ids = bus_stop_dao.get_bus_stops_by_ids(bus_stop_ids)[1]
    if new_bus_stop_ids:
        err_msg = '%d new bus stops need to be created, please use the Bus Stop Add function first : %s' % (len(new_bus_stop_ids), ','.join(new_bus_stop_ids))
        _logger.error(err_msg)
        raise PTPValueError(err_msg)

    return bus_routes_after_rules


def sequence_check_between_ncs_and_lta(bus_routes_ncs, bus_routes_lta):
    bus_service_not_match_ids = []
    if len(bus_routes_ncs) == len(bus_routes_lta):
        for bus_route_ncs, bus_route_lta in zip(bus_routes_ncs, bus_routes_lta):
            if len(bus_route_ncs) == len(bus_route_lta):
                for route_ncs, route_lta in zip(bus_route_ncs, bus_route_lta):
                    if (route_ncs[1], route_ncs[2], route_ncs[3]) != (route_lta[1], route_lta[2], route_lta[3]):
                        bus_service_not_match_ids.append(route_ncs[0])
                        break
            else:
                bus_service_not_match_ids.append(bus_route_ncs[0][0])
    else:
        err_msg = 'Numbers of bus services retrieved from CSV files are different: %d services for NCS, %d services for LTA' % (len(bus_routes_ncs), len(bus_routes_lta))
        _logger.error(err_msg)
        raise PTPValueError(err_msg)

    if bus_service_not_match_ids:
        err_msg = 'Bus sequences of %d bus services do not match between NCS and LTA sets: %s' % (len(bus_service_not_match_ids), ','.join(bus_service_not_match_ids))
        _logger.error(err_msg)
        raise PTPValueError(err_msg)


def generate_sql(bus_routes_ncs, bus_routes_lta):
    sql = ''
    for bus_route in bus_routes_ncs:
        sql += "DELETE FROM bus_routes WHERE bus_service_id = %s AND provider = 'NCS';\n" % bus_route[0][0]
        for route in bus_route:
            sql += "INSERT INTO bus_routes (bus_service_id, direction, sequence, bus_stop_id, provider, express_code, distance, distance_fares_marker, weekday_first_trip, weekday_last_trip, saturday_first_trip, saturday_last_trip, sunday_first_trip, sunday_last_trip, note, shows_arrival_table, shows_fare_table, in_operation) VALUES (%s, %s, %s, %s, 'NCS', %s, %s, NULL, %s, %s, %s, %s, %s, %s, NULL, '0', '0', '1');\n" % (route[0], route[1], route[2], route[3], route[4], route[5], route[6], route[7], route[8], route[9], route[10], route[11])
    for bus_route in bus_routes_lta:
        sql += "DELETE FROM bus_routes WHERE bus_service_id = %s AND provider = 'LTA';\n" % bus_route[0][0]
        for route in bus_route:
            sql += "INSERT INTO bus_routes (bus_service_id, direction, sequence, bus_stop_id, provider, express_code, distance, distance_fares_marker, weekday_first_trip, weekday_last_trip, saturday_first_trip, saturday_last_trip, sunday_first_trip, sunday_last_trip, note, shows_arrival_table, shows_fare_table, in_operation) VALUES (%s, %s, %s, %s, 'LTA', %s, %s, %s, NULL, NULL, NULL, NULL, NULL, NULL, NULL, '0', '0', '1');\n" % (route[0], route[1], route[2], route[3], route[4], route[5], route[6])
    return sql