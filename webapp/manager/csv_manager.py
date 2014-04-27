import logging
import os
import re
from webapp import config
from webapp.exceptions import PTPValueError
from webapp.util import io_util

__author__ = 'Gao Lei'

_logger = logging.getLogger('default')


def _bus_service_id_rule(string):
    return re.sub('^[0]+', '', string)


def _bus_stop_code_rule(origin_bus_stop_code):
    pattern = r'^\d{4}$'
    if re.search(pattern, origin_bus_stop_code):
        offset = '0' * (5 - len(origin_bus_stop_code))
        target_bus_stop_code = '%s%s' % (offset,  origin_bus_stop_code)
    else:
        target_bus_stop_code = origin_bus_stop_code
    return target_bus_stop_code


def get_csv_list(csv_type=None):
    csv_folder = config.CSV_FOLDER
    io_util.create_folder_if_not_exists(csv_folder)
    csv_list = [f for f in os.listdir(csv_folder) if os.path.isfile(os.path.join(csv_folder, f)) and f.lower().endswith('.csv')]
    # CSV type filter
    if csv_type:
        csv_list = [f for f in csv_list if '[%s]' % csv_type in f]
    # sort by date reversed
    csv_list.sort(key=lambda x: os.path.getmtime(os.path.join(csv_folder, x)), reverse=True)
    return csv_list


def save_csv(csv_file, csv_type, sr_number):
    csv_name = '[%s][%s]%s' % (sr_number, csv_type, csv_file.name)
    csv_path = os.path.join(config.CSV_FOLDER, csv_name)
    io_util.write_to_file(csv_path, csv_file)
    _logger.info('CSV file saved: %s' % csv_path)


def retrieve_multiple_data_from_csv(csv_name, csv_type, filter_ids):
    multiple_data = []
    filter_ids_missing = set()
    for filter_id in filter_ids:
        data = retrieve_data_from_csv(csv_name, csv_type, filter_id)
        if data:
            multiple_data.append(data)
        else:
            filter_ids_missing.add(filter_id)
    return multiple_data, filter_ids_missing


def retrieve_data_from_csv(csv_name, csv_type, filter_id=None):
    csv_path = os.path.join(config.CSV_FOLDER, csv_name)
    data = []
    try:
        with open(csv_path, 'r') as reader:
            for line in reader:
                row = [item.strip() for item in line.split(',')]
                if csv_type == 'BUS_STOP':
                    # bus stop code process
                    row[0] = _bus_stop_code_rule(row[0])
                    if row[0] == filter_id:
                        data = row
                        break
                elif csv_type in ('BUS_SERVICE', 'BUS_ROUTE_NCS', 'BUS_ROUTE_LTA'):
                    # bus service id process
                    row[0] = _bus_service_id_rule(row[0])
                    if row[0] == filter_id:
                        data.append(row)
                else:
                    data.append(row)

        _logger.info('Data retrieved from CSV successfully: %s' % csv_path)
    except Exception, ex:
        err_msg = 'An error occurred while retrieving data from CSV %s: %s' % (csv_path, ex)
        _logger.error(err_msg)
        raise PTPValueError(err_msg)
    return data


def delete(csv_name):
    csv_path = os.path.join(config.CSV_FOLDER, csv_name)
    io_util.delete_file(csv_path)