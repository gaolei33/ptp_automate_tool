import os

__author__ = 'Gao Lei'


DB_INFO = {
    'HOST': '127.0.0.1',
    'PORT': 3306,
    'NAME': 'test',
    'USER': 'root',
    'PASSWORD': '880428'
}

MENUS = (
    {'TITLE': 'DB', 'LINK': '/webapp/db/',
        'SUBMENUS': (
            {'TITLE': 'DB Backup', 'LINK': '/webapp/db/db_backup/'},
            {'TITLE': 'DB Restore', 'LINK': '/webapp/db/db_restore/'},
            {'TITLE': 'DB Backup Delete', 'LINK': '/webapp/db/db_backup_delete/'},
        )
    },
    {'TITLE': 'CSV', 'LINK': '/webapp/csv/',
        'SUBMENUS': (
            {'TITLE': 'CSV Upload', 'LINK': '/webapp/csv/csv_upload/'},
            {'TITLE': 'CSV Delete', 'LINK': '/webapp/csv/csv_delete/'},
        )
    },
    {'TITLE': 'Bus Stop', 'LINK': '/webapp/bus_stop/',
        'SUBMENUS': (
            {'TITLE': 'Bus Stop Add', 'LINK': '/webapp/bus_stop/bus_stop_add/'},
            {'TITLE': 'Bus Stop Update', 'LINK': '/webapp/bus_stop/bus_stop_update/'},
        )
    },
    {'TITLE': 'Bus Service', 'LINK': '/webapp/bus_service/',
        'SUBMENUS': (
            {'TITLE': 'Bus Service Add / Update', 'LINK': '/webapp/bus_service/bus_service_add_or_update/'},
            {'TITLE': 'Bus Service Enable / Disable', 'LINK': '/webapp/bus_service/bus_service_enable_or_disable/'},
        )
    },
    {'TITLE': 'Bus Route', 'LINK': '/webapp/bus_route/',
        'SUBMENUS': (
            {'TITLE': 'Bus Route NCS', 'LINK': '/webapp/bus_route/bus_route_ncs/'},
            {'TITLE': 'Bus Route LTA', 'LINK': '/webapp/bus_route/bus_route_lta/'},
        )
    },
    {'TITLE': 'SQL', 'LINK': '/webapp/sql/',
        'SUBMENUS': (
            {'TITLE': 'SQL Download', 'LINK': '/webapp/sql/sql_download/'},
            {'TITLE': 'SQL Delete', 'LINK': '/webapp/sql/sql_delete/'},
        )
    },
    {'TITLE': 'Street Search', 'LINK': 'javascript: street_search_toggle();', 'ALIGN': 'right'},
)

ROOT = '/home/jonathan/Desktop/ptp_automate_tool'

CSV_FOLDER = os.path.join(ROOT, 'csv')

# CSV_FOLDERS = {
#     'BUS_STOP': os.path.join(CSV_ROOT, 'BUS_STOP'),
#     'BUS_SERVICE': os.path.join(CSV_ROOT, 'BUS_SERVICE'),
#     'BUS_ROUTE_NCS': os.path.join(CSV_ROOT, 'BUS_ROUTE_NCS'),
#     'BUS_ROUTE_LTA': os.path.join(CSV_ROOT, 'BUS_ROUTE_LTA'),
# }

BACKUP_FOLDER = os.path.join(ROOT, 'backup')

BACKUP_TABLES = (
    'bus_services',
    'bus_service_directions',
    'bus_service_loops',
    'bus_routes',
    'bus_stops',
)

SQL_FOLDER = os.path.join(ROOT, 'sql')


def my_context_processor(request):
    return {
        'MENUS': MENUS,
    }