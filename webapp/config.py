import os

__author__ = 'Gao Lei'

DB_INFO = {
        'HOST': '127.0.0.1',
        'PORT': 3306,
        'NAME': 'test',
        'USER': 'root',
        'PASSWORD': '880428'
}

BUS_STOP = 'bus_stop'
BUS_SERVICE = 'bus_service'
BUS_ROUTE_NCS = 'bus_route_ncs'
BUS_ROUTE_LTA = 'bus_route_lta'

ROOT = '/home/jonathan/Desktop/ptp_automate_tool'

# The path of the CSV folder
CSV_ROOT = os.path.join(ROOT, 'csv')
CSV_FOLDERS = {
    'BUS_STOP': os.path.join(CSV_ROOT, 'BUS_STOP'),
    'BUS_SERVICE': os.path.join(CSV_ROOT, 'BUS_SERVICE'),
    'BUS_ROUTE_NCS': os.path.join(CSV_ROOT, 'BUS_ROUTE_NCS'),
    'BUS_ROUTE_LTA': os.path.join(CSV_ROOT, 'BUS_ROUTE_LTA'),
}

BACKUP_FOLDER = os.path.join(ROOT, '/home/jonathan/Desktop/ptp_automate_tool/backup')
BACKUP_TABLES = 'bus_services bus_service_directions bus_service_loops bus_routes bus_stops'
SQL_FOLDER = os.path.join(ROOT, 'sql')