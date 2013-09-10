import os

__author__ = 'Gao Lei'


MODE_SWITCHER = 'SERVER'

DEBUGS = {
    'SERVER': False,
    'LOCAL': True,
}

DB_INFOS = {
    'SERVER': {
        'HOST': '127.0.0.1',
        'PORT': 3306,
        'NAMES': 'ptp2',
        'USER': 'developer',
        'PASSWORD': 'password'
    },
    'LOCAL': {
        'HOST': '127.0.0.1',
        'PORT': 3306,
        'NAMES': 'ptp2',
        'USER': 'root',
        'PASSWORD': '880428',
    }
}

ROOTS = {
    'SERVER': '/media/ext/Public/share/ptp_automate_tool',
    'LOCAL': '/home/jonathan/Desktop/ptp_automate_tool',
}

DEBUG = DEBUGS[MODE_SWITCHER]

DB_INFO = DB_INFOS[MODE_SWITCHER]

ROOT = ROOTS[MODE_SWITCHER]

CSV_FOLDER = os.path.join(ROOT, 'csv')

BACKUP_FOLDER = os.path.join(ROOT, 'backup')

BACKUP_TABLES = (
    'bus_stops',
    'bus_services',
    'bus_service_directions',
    'bus_service_loops',
    'bus_routes',
    'bus_route_polylines',
)

SQL_FOLDER = os.path.join(ROOT, 'sql')

PDF_RENAME_PATTERN = r'_\d_Index'

PDF_ROOT = 'pdf/roadIndex/'

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
    {'TITLE': 'PDF Rename', 'LINK': '/webapp/pdf/'},
    {'TITLE': 'HTML & SHP & KML Tools', 'LINK': 'http://192.168.152.135:8381/publictransport-maintenance/', 'TARGET': '_blank'},
    {'TITLE': 'Street Search', 'LINK': 'javascript: street_search_toggle();', 'ALIGN': 'right'},
)

BUS_STOP_SHORT_NAME_LONG_NAME_MAP = {
    'admin': 'Administration',
    'amk': 'Ang Mo Kio',
    'apt': 'Apartment',
    'assn': 'Association',
    'ave': 'Avenue',
    'aye': 'Ayer Rajah Expressway',
    'bke': 'Bukit Timah Expressway',
    'bldg': 'Building',
    'blk': 'Block',
    'blvd': 'Boulevard',
    'bo': 'Branch Office',
    'br': 'Branch',
    'bt': 'Bukit',
    'c\'wealth': 'Commonwealth',
    'cath': 'Cathedral',
    'cbd': 'Central Business District',
    'cc': 'Community',
    'cck': 'Choa Chu Kang',
    'cemy': 'Cemetery',
    'ch': 'Church',
    'cine': 'Cinema',
    'cl': 'Close',
    'clubhse': 'Clubhouse',
    'cmplx': 'Complex',
    'condo': 'Condominium',
    'cres': 'Crescent',
    'ct': 'Court',
    'cte': 'Central Expressway',
    'ctr': 'Centre',
    'ctrl': 'Central',
    'dr': 'Drive',
    'e\'way': 'Expressway',
    'ecp': 'East Coast Parkway',
    'env': 'Environment',
    'est': 'Estate',
    'fc': 'Food Centre',
    'gdn': 'Garden',
    'govt': 'Government',
    'gr': 'Grove',
    'hts': 'Heights',
    'ind': 'Industrial',
    'inst': 'Institute',
    'instn': 'Institution',
    'jln': 'Jalan',
    'jnr': 'Junior',
    'kg': 'Kampong',
    'kje': 'Kranji Expressway',
    'kt': 'Katong',
    'lib': 'Library',
    'lk': 'Link',
    'lor': 'Lorong',
    'meth': 'Methodist',
    'mjd': 'Masjid',
    'mkt': 'Market',
    'mt': 'Mount',
    'n\'hood': 'Neightbourhood',
    'natl': 'National',
    'npc': 'Neightbourhood Police Center',
    'npp': 'Neightbourhood Police Post',
    'nth': 'North',
    'opp': 'Opposite',
    'pie': 'Pan-Island Expressway',
    'pk': 'Park',
    'poly': 'Polyclinic',
    'pr': 'Primary',
    'pt': 'Point',
    'rd': 'Road',
    's\'pore': 'Singapore',
    'sch': 'School',
    'sec': 'Secondary',
    'sle': 'Seletar Expressway',
    'sq': 'Square',
    'st': 'Street',
    'sth': 'South',
    'stn': 'Station',
    'tc': 'Town Council',
    'tech': 'Technical',
    'ter': 'Terrace',
    'tg': 'Tanjong',
    'tpe': 'Tampines Expressway',
    'upp': 'Upper',
    'voc': 'Vocational',
}

def my_context_processor(request):
    return {
        'MENUS': MENUS,
    }