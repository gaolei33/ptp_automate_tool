from webapp.util import db_util

__author__ = 'Gao Lei'


def get_missing_bus_service_ids(bus_service_ids):
    bus_service_ids_string_wrap_quotes = ', '.join(["'%s'" % bus_service_id for bus_service_id in bus_service_ids])
    sql = "SELECT CONCAT(id) FROM bus_services WHERE id IN (%s);" % bus_service_ids_string_wrap_quotes

    result = db_util.exec_query(sql)

    bus_service_ids_found = {bus_service[0] for bus_service in result}
    bus_service_ids_missing = bus_service_ids - bus_service_ids_found

    return bus_service_ids_missing


def get_missing_directions(directions):
    directions_string_wrap_quotes = ', '.join(["('%s', '%s')" % (direction[0], direction[1]) for direction in directions])
    sql = "SELECT CONCAT(bus_service_id), CONCAT(direction) FROM bus_service_directions WHERE (bus_service_id, direction) IN (%s);" % directions_string_wrap_quotes

    result = db_util.exec_query(sql)

    directions_found = set(result)
    directions_missing = directions - directions_found

    return directions_missing