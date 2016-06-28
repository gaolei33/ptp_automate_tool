from django.views.generic.base import RedirectView
from django.conf.urls import url

from webapp.view import db_view
from webapp.view import csv_view
from webapp.view import bus_stop_view
from webapp.view import bus_service_view
from webapp.view import bus_route_view
from webapp.view import address_view
from webapp.view import pdf_view
from webapp.view import sql_view
from webapp.view import street_view
from webapp.view import html_shp_kml_view

__author__ = 'Gao Lei'


urlpatterns = [
    url(r'^$', RedirectView.as_view(url='/webapp/db/')),
]

urlpatterns += [
    url(r'^db/$', RedirectView.as_view(url='/webapp/db/db_backup/')),
    url(r'^db/db_backup/$', db_view.db_home, {'method': 'DB_BACKUP', 'description': 'DB Backup'}),
    url(r'^db/db_restore/$', db_view.db_home, {'method': 'DB_RESTORE', 'description': 'DB Restore'}),
    url(r'^db/db_backup_delete/$', db_view.db_home, {'method': 'DB_BACKUP_DELETE', 'description': 'DB Backup Delete'}),
    url(r'^db/db_handler/$', db_view.db_handler),
]

urlpatterns += [
    url(r'^csv/$', RedirectView.as_view(url='/webapp/csv/csv_upload/')),
    url(r'^csv/csv_upload/$', csv_view.csv_home, {'method': 'CSV_UPLOAD', 'description': 'CSV Upload'}),
    url(r'^csv/csv_delete/$', csv_view.csv_home, {'method': 'CSV_DELETE', 'description': 'CSV Delete'}),
    url(r'^csv/csv_handler/$', csv_view.csv_handler),
]

urlpatterns += [
    url(r'^bus_stop/$', RedirectView.as_view(url='/webapp/bus_stop/bus_stop_add/')),
    url(r'^bus_stop/bus_stop_add/$', bus_stop_view.bus_stop_home, {'method': 'BUS_STOP_ADD', 'description': 'Bus Stop Add'}),
    url(r'^bus_stop/bus_stop_update/$', bus_stop_view.bus_stop_home, {'method': 'BUS_STOP_UPDATE', 'description': 'Bus Stop Update'}),
    url(r'^bus_stop/bus_stop_detail/$', bus_stop_view.bus_stop_detail),
    url(r'^bus_stop/bus_stop_handler/$', bus_stop_view.bus_stop_handler),
]

urlpatterns += [
    url(r'^bus_service/$', RedirectView.as_view(url='/webapp/bus_service/bus_service_add_or_update/')),
    url(r'^bus_service/bus_service_add_or_update/$', bus_service_view.bus_service_home, {'method': 'BUS_SERVICE_ADD_OR_UPDATE', 'description': 'Bus Service Add / Update'}),
    url(r'^bus_service/bus_service_enable_or_disable/$', bus_service_view.bus_service_home, {'method': 'BUS_SERVICE_ENABLE_OR_DISABLE', 'description': 'Bus Service Enable / Disable'}),
    url(r'^bus_service/bus_service_handler/$', bus_service_view.bus_service_handler),
]

urlpatterns += [
    url(r'^bus_route/$', RedirectView.as_view(url='/webapp/bus_route/bus_route_add_or_update/')),
    url(r'^bus_route/bus_route_add_or_update/$', bus_route_view.bus_route_home, {'method': 'BUS_ROUTE_ADD_OR_UPDATE', 'description': 'Bus Route Add / Update'}),
    url(r'^bus_route/bus_route_handler/$', bus_route_view.bus_route_handler),
]

urlpatterns += [
    url(r'^address/$', RedirectView.as_view(url='/webapp/address/address_add/')),
    url(r'^address/address_add/$', address_view.address_home, {'method': 'ADDRESS_ADD', 'description': 'Address Add'}),
    url(r'^address/address_detail/$', address_view.address_detail),
    url(r'^address/address_handler/$', address_view.address_handler),
]

urlpatterns += [
    url(r'^sql/$', RedirectView.as_view(url='/webapp/sql/sql_download/')),
    url(r'^sql/sql_download/$', sql_view.sql_home, {'method': 'SQL_DOWNLOAD', 'description': 'SQL Download'}),
    url(r'^sql/sql_merged_download/$', sql_view.sql_home, {'method': 'SQL_MERGED_DOWNLOAD', 'description': 'SQL Merged Download'}),
    url(r'^sql/sql_delete/$', sql_view.sql_home, {'method': 'SQL_DELETE', 'description': 'SQL Delete'}),
    url(r'^sql/sql_handler/$', sql_view.sql_handler),
]

urlpatterns += [
    url(r'^pdf/$', RedirectView.as_view(url='/webapp/pdf/pdf_rename/')),
    url(r'^pdf/pdf_rename/$', pdf_view.pdf_home, {'method': 'PDF_RENAME', 'description': 'PDF Rename'}),
    url(r'^pdf/pdf_handler/$', pdf_view.pdf_handler),
]

urlpatterns += [
    url(r'^street/street_search/$', street_view.street_search),
]

urlpatterns += [
    url(r'^html_shp_kml/$', html_shp_kml_view.html_shp_kml_home, {'description': 'HTML & SHP & KML'}),
]