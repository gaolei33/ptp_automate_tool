import logging
from webapp.common import db_utils
from webapp.common.io import csv_manager

__author__ = 'Gao Lei'

_logger = logging.getLogger('default')

def get_bus_stop_info(csv_name, bus_stop_ids):

    total_bus_stop_info = list()

    missing_bus_stop_ids = set()

    # retrieve data from CSV
    for bus_stop_id in bus_stop_ids:
        bus_stop_info = csv_manager.retrieve_data_from_csv(csv_name, 'BUS_STOP', bus_stop_id)

        street_ids = street_search(bus_stop_info['DATA'][0][1], 'short_name')
        street_id = street_ids[0][0]  if street_ids else ''
        bus_stop_info['DATA'][0][1] = street_id

        total_bus_stop_info.append(bus_stop_info)

        if not bus_stop_info['DATA']:
            missing_bus_stop_ids.add(bus_stop_info['ID'])

    # incorrect bus stop check
    if missing_bus_stop_ids:
        missing_bus_stop_idss_string = ','.join(missing_bus_stop_ids)
        err_msg = 'Bus stops %s cannot be found in %s' % (missing_bus_stop_idss_string, csv_name)
        _logger.error(err_msg)
        raise ValueError(err_msg)

    return total_bus_stop_info

def street_search(keyword, keywod_type):

    try:
        connection = db_utils.get_connection()
        cursor = connection.cursor()
        cursor.execute("select id, short_name, long_name from streets where %s like '%%%s%%' limit 100" % (keywod_type, keyword))
        result = cursor.fetchall()
        cursor.close()
        db_utils.close_connection(connection)
    except Exception, ex:
        err_msg = 'An error occurred while searching street: %s' % ex
        _logger.error(err_msg)
        raise ValueError(err_msg)

    return result