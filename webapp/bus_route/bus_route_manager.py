import logging
import re
import time
from webapp.bus_route.ncs_set.data_rule import Rule
from webapp import config
from webapp.common import db_utils
from webapp.common.io import sql_manager, csv_manager, io_utils

__author__ = 'Gao Lei'

_logger = logging.getLogger('default')

def bus_route_update(csv_name, csv_type, bus_service_ids):

    total_bus_routes = list()

    missing_bus_service_ids = set()

    # retrieve data from CSV
    for bus_service_id in bus_service_ids:
        bus_routes = csv_manager.retrieve_data_from_csv(csv_name, csv_type, bus_service_id)
        total_bus_routes.append(bus_routes)
        if not bus_routes['DATA']:
            missing_bus_service_ids.add(bus_routes['ID'])

    # incorrect bus service check
    if missing_bus_service_ids:
        missing_bus_service_ids_string = ','.join(missing_bus_service_ids)
        err_msg = 'Bus routes of bus services %s cannot be found in %s' % (missing_bus_service_ids_string, csv_name)
        _logger.error(err_msg)
        raise ValueError(err_msg)

    # new bus stops check
    bus_stops = { bus_route[3] for bus_routes in total_bus_routes for bus_route in bus_routes['DATA']  }
    new_bus_stops = select_new_bus_stops(bus_stops)
    if new_bus_stops:
        new_bus_stops_string = ','.join(new_bus_stops)
        err_msg = 'New bus stops need to be created: %s' % new_bus_stops_string
        _logger.error(err_msg)
        raise ValueError(err_msg)

    # auto amend bus bus_routes data
    rule = Rule(total_bus_routes)
    bus_routes_after_rules = rule.execute_rules()

    # generate SQL string
    sql = generate_sql(bus_routes_after_rules, csv_type)

    # execute the generated SQL on development database
    cmd = 'mysql -h %s -u %s -p%s %s -e "%s"' % (config.DB_INFO['HOST'], config.DB_INFO['USER'], config.DB_INFO['PASSWORD'], config.DB_INFO['NAME'], sql)
    error = io_utils.exec_cmd(cmd)
    if error:
        err_msg = 'An error occurred while executing the SQL: %s, you\'d better restore development database before next steps.' % error
        _logger.error(err_msg)
        raise ValueError(err_msg)

    # save SQL string to file
    current_time = time.strftime('%Y%m%d%H%M%S')
    sr_number = get_sr_number(csv_name)
    sql_name = 'SR_%s_%s_%s_%s.sql' % (sr_number, csv_type, '_'.join(bus_service_ids), current_time)
    sql_manager.save_sql(sql_name, sql)


def select_new_bus_stops(bus_stops):

    try:
        new_bus_stops = set()
        connection = db_utils.get_connection()
        cursor = connection.cursor()
        for stop in bus_stops:
            cursor.execute("select * from bus_stops where id = '%s'" % stop)
            result = cursor.fetchone()
            if result == None:
                new_bus_stops.add(stop)
        cursor.close()
        db_utils.close_connection(connection)
    except Exception, ex:
        err_msg = 'An error occurred while checking new bus stops: %s' % ex
        _logger.error(err_msg)
        raise ValueError(err_msg)

    return new_bus_stops


def generate_sql(total_bus_routes, csv_type):

    sql = ''

    for bus_routes in total_bus_routes:

        if csv_type == 'BUS_ROUTE_NCS':
            sql += "DELETE FROM bus_routes WHERE bus_service_id = '%s' AND provider = 'NCS';\n" % bus_routes['ID']
            for bus_route in bus_routes['DATA']:
                sql += "INSERT INTO bus_routes (bus_service_id, direction, sequence, bus_stop_id, provider, express_code, distance, distance_fares_marker, weekday_first_trip, weekday_last_trip, saturday_first_trip, saturday_last_trip, sunday_first_trip, sunday_last_trip, note, shows_arrival_table, shows_fare_table, in_operation) VALUES(%s, %s, %s, %s, 'NCS', %s, %s, NULL, %s, %s, %s, %s, %s, %s, NULL, '0', '0', '1');\n" % (bus_route[0], bus_route[1], bus_route[2], bus_route[3], bus_route[4], bus_route[5], bus_route[6], bus_route[7], bus_route[8], bus_route[9], bus_route[10], bus_route[11])

        elif csv_type == 'BUS_ROUTE_LTA':
            sql += "DELETE FROM bus_routes WHERE bus_service_id = '%s' AND provider = 'LTA';\n" % bus_routes['ID']
            for bus_route in bus_routes['DATA']:
                sql += "INSERT INTO bus_routes (bus_service_id, direction, sequence, bus_stop_id, provider, express_code, distance, distance_fares_marker, weekday_first_trip, weekday_last_trip, saturday_first_trip, saturday_last_trip, sunday_first_trip, sunday_last_trip, note, shows_arrival_table, shows_fare_table, in_operation) VALUES(%s, %s, %s, %s, 'LTA', %s, %s, %s, NULL, NULL, NULL, NULL, NULL, NULL, NULL, '0', '0', '1');\n" % (bus_route[0], bus_route[1], bus_route[2], bus_route[3], bus_route[4], bus_route[5], bus_route[6])

    return sql


def get_sr_number(csv_name):

    m = re.search(r'^SR_(\d+)_', csv_name)

    if m:
        sr_number = m.group(1)
    else:
        sr_number = 'Unknown'

    return sr_number
