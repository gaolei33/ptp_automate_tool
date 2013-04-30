import logging
import os
import re
from webapp import config
from webapp.util import io_utils

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


def get_csv_list(csv_type):
    csv_folder = config.CSV_FOLDERS[csv_type]
    io_utils.create_folder_if_not_exists(csv_folder)
    csv_list = [f for f in os.listdir(csv_folder) if os.path.isfile(os.path.join(csv_folder, f)) and f.lower().endswith('.csv')]
    return csv_list


def save_csv(csv_file, csv_type, sr_number):
    csv_folder = config.CSV_FOLDERS[csv_type]
    csv_name = 'SR_%s_%s' % (sr_number, csv_file.name)
    csv_path = os.path.join(csv_folder, csv_name)
    io_utils.write_to_file(csv_path, csv_file)
    _logger.info('CSV file saved: %s' % csv_path)


def retrieve_data_from_csv(csv_name, csv_type, filter_id):
    csv_folder = config.CSV_FOLDERS[csv_type]
    csv_path = os.path.join(csv_folder, csv_name)
    info = {
        'ID': filter_id,
        'DATA': [],
    }
    try:
        with open(csv_path, 'r') as reader:
            for line in reader:
                row = [item.strip() for item in line.strip().split(',')]
                # bus service id & bus stop code process
                row[0] = _bus_stop_code_rule(row[0]) if csv_type == 'BUS_STOP' else _bus_service_id_rule(row[0])
                if row[0] == filter_id:
                    info['DATA'].append(row)
        _logger.info('Data retrieved from CSV successfully: %s' % csv_path)
    except Exception, ex:
        err_msg = 'An error occurred while retrieving data from CSV %s: %s' % (csv_path, ex)
        _logger.error(err_msg)
        raise ValueError(err_msg)
    return info