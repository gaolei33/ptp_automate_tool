import logging
import MySQLdb
import time
from webapp.bus_route.ncs_set import sql_generator
from webapp.bus_route.ncs_set.data_rule import Rule
from webapp import config
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
    sql = sql_generator.generate_sql(bus_routes_after_rules)

    # execute the generated SQL on development database
    cmd = 'mysql -h %s -u %s -p%s %s -e "%s"' % (
    config.DB_INFO['HOST'], config.DB_INFO['USER'], config.DB_INFO['PASSWORD'], config.DB_INFO['NAME'], sql)
    error = io_utils.exec_cmd(cmd)
    if error:
        err_msg = 'An error occurred while executing the SQL: %s' % error
        raise ValueError(err_msg)

    # save SQL string to file
    current_time = time.strftime('%Y%m%d%H%M%S')
    sql_name = 'bus_route_update_%s_%s.sql' % ('_'.join(bus_service_ids), current_time)
    sql_manager.save_sql(sql_name, sql)


def select_new_bus_stops(bus_stops):

    try:
        new_bus_stops = set()
        connection = MySQLdb.connect(config.DB_INFO['HOST'], config.DB_INFO['USER'], config.DB_INFO['PASSWORD'], config.DB_INFO['NAME'], config.DB_INFO['PORT'])
        cursor = connection.cursor()
        for stop in bus_stops:
            cursor.execute("select * from bus_stops where id = '%s'" % stop)
            result = cursor.fetchone()
            if result == None:
                new_bus_stops.add(stop)
        cursor.close()
        connection.close()
    except Exception, ex:
        err_msg = 'An error occurred while checking new bus stops: %s' % ex
        _logger.error(err_msg)
        raise ValueError(err_msg)

    return new_bus_stops
