from webapp.util import db_util

__author__ = 'Gao Lei'


def get_bus_stops_by_ids(bus_stop_ids):
    bus_stop_ids_string_wrap_quotes = ', '.join({"'%s'" % bus_stop_id for bus_stop_id in bus_stop_ids})
    sql = "SELECT CONCAT(id), CONCAT(street_id), CONCAT(long_name), CONCAT(short_name), IF(location_code IS NULL, '', CONCAT(location_code)), CONCAT(is_wab_accessible), CONCAT(is_non_bus_stop), CONCAT(is_interchange), CONCAT(longitude), CONCAT(latitude) FROM bus_stops WHERE id IN (%s);" % bus_stop_ids_string_wrap_quotes

    result = db_util.exec_query(sql)

    bus_stop_ids_found = {bus_stop[0] for bus_stop in result}
    bus_stop_ids_missing = bus_stop_ids - bus_stop_ids_found

    return result, bus_stop_ids_missing