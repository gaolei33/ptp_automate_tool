import os

__author__ = 'Gao Lei'


ENV = 'server'

CONFIG = {
    'server': {
        'debug': False,
        'db': {
            'host': '127.0.0.1',
            'user': 'developer',
            'password': 'password',
            'database': 'ptp2',
        },
        'root': '/media/ext/Public/share/ptp_automate_tool',
    },
    'local': {
        'debug': True,
        'db': {
            'host': '127.0.0.1',
            'user': 'root',
            'password': '880428',
            'database': 'ptp2',
        },
        'root': '/home/jonathan/Desktop/ptp_automate_tool',
    },
}

DEBUG = CONFIG[ENV]['debug']

DB = CONFIG[ENV]['db']

ROOT = CONFIG[ENV]['root']

CSV_FOLDER = os.path.join(ROOT, 'csv')

BACKUP_FOLDER = os.path.join(ROOT, 'backup')

#BACKUP_TABLES = (
#    'bus_stops',
#    'bus_services',
#    'bus_service_directions',
#    'bus_service_loops',
#    'bus_routes',
#    'bus_route_polylines',
#    'addresses',
#)

SQL_FOLDER = os.path.join(ROOT, 'sql')

PDF_RENAME_PATTERN = r'_\d_Index'

PDF_ROOT = 'pdf/roadIndex/'

MENUS = (
    {
        'title': 'DB', 'link': '/webapp/db/',
        'submenus': (
            {'title': 'DB Backup', 'link': '/webapp/db/db_backup/'},
            {'title': 'DB Restore', 'link': '/webapp/db/db_restore/'},
            {'title': 'DB Backup Delete', 'link': '/webapp/db/db_backup_delete/'},
        )
    },
    {
        'title': 'CSV', 'link': '/webapp/csv/',
        'submenus': (
            {'title': 'CSV Upload', 'link': '/webapp/csv/csv_upload/'},
            {'title': 'CSV Delete', 'link': '/webapp/csv/csv_delete/'},
        )
    },
    {
        'title': 'Bus Stop', 'link': '/webapp/bus_stop/',
        'submenus': (
            {'title': 'Bus Stop Add', 'link': '/webapp/bus_stop/bus_stop_add/'},
            {'title': 'Bus Stop Update', 'link': '/webapp/bus_stop/bus_stop_update/'},
        )
    },
    {
        'title': 'Bus Service', 'link': '/webapp/bus_service/',
        'submenus': (
            {'title': 'Bus Service Add / Update', 'link': '/webapp/bus_service/bus_service_add_or_update/'},
            {'title': 'Bus Service Enable / Disable', 'link': '/webapp/bus_service/bus_service_enable_or_disable/'},
        )
    },
    {
        'title': 'Bus Route', 'link': '/webapp/bus_route/',
        'submenus': (
            {'title': 'Bus Route Add / Update', 'link': '/webapp/bus_route/bus_route_add_or_update/'},
        )
    },
    {
        'title': 'Address', 'link': '/webapp/address/',
        'submenus': (
            {'title': 'Address Add', 'link': '/webapp/address/address_add/'},
        )
    },
    {
        'title': 'SQL', 'link': '/webapp/sql/',
        'submenus': (
            {'title': 'SQL Download', 'link': '/webapp/sql/sql_download/'},
            {'title': 'SQL Merged Download', 'link': '/webapp/sql/sql_merged_download/'},
            {'title': 'SQL Delete', 'link': '/webapp/sql/sql_delete/'},
        )
    },
    {
        'title': 'PDF', 'link': '/webapp/pdf/',
        'submenus': (
            {'title': 'PDF Rename', 'link': '/webapp/pdf/pdf_rename/'},
        )
    },
    {'title': 'HTML & SHP & KML Tools', 'link': 'http://192.168.152.135:8381/publictransport-maintenance/', 'target': '_blank'},
    {'title': 'Street Search', 'link': 'javascript: street_search_toggle();', 'align': 'right'},
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
        'menus': MENUS,
    }