from django.views.generic.base import RedirectView
from django.conf.urls import patterns, url

__author__ = 'Gao Lei'


urlpatterns = patterns('',
    url(r'^$', RedirectView.as_view(url='/webapp/db/')),
)

urlpatterns += patterns('webapp.view.db_view',
    url(r'^db/$', RedirectView.as_view(url='/webapp/db/db_backup/')),
    url(r'^db/db_backup/$', 'db_home', {'method': 'DB_BACKUP', 'description': 'DB Backup'}),
    url(r'^db/db_restore/$', 'db_home', {'method': 'DB_RESTORE', 'description': 'DB Restore'}),
    url(r'^db/db_backup_delete/$', 'db_home', {'method': 'DB_BACKUP_DELETE', 'description': 'DB Backup Delete'}),
    url(r'^db/db_handler/$', 'db_handler'),
)

urlpatterns += patterns('webapp.view.csv_view',
    url(r'^csv/$', RedirectView.as_view(url='/webapp/csv/csv_upload/')),
    url(r'^csv/csv_upload/$', 'csv_home', {'method': 'CSV_UPLOAD', 'description': 'CSV Upload'}),
    url(r'^csv/csv_delete/$', 'csv_home', {'method': 'CSV_DELETE', 'description': 'CSV Delete'}),
    url(r'^csv/csv_handler/$', 'csv_handler'),
)

urlpatterns += patterns('webapp.view.bus_stop_view',
    url(r'^bus_stop/$', RedirectView.as_view(url='/webapp/bus_stop/bus_stop_add/')),
    url(r'^bus_stop/bus_stop_add/$', 'bus_stop_home', {'method': 'BUS_STOP_ADD', 'description': 'Bus Stop Add'}),
    url(r'^bus_stop/bus_stop_update/$', 'bus_stop_home', {'method': 'BUS_STOP_UPDATE', 'description': 'Bus Stop Update'}),
    url(r'^bus_stop/bus_stop_detail/$', 'bus_stop_detail'),
    url(r'^bus_stop/bus_stop_handler/$', 'bus_stop_handler'),
)

urlpatterns += patterns('webapp.view.bus_service_view',
    url(r'^bus_service/$', RedirectView.as_view(url='/webapp/bus_service/bus_service_add_or_update/')),
    url(r'^bus_service/bus_service_add_or_update/$', 'bus_service_home', {'method': 'BUS_SERVICE_ADD_OR_UPDATE', 'description': 'Bus Service Add / Update'}),
    url(r'^bus_service/bus_service_enable_or_disable/$', 'bus_service_home', {'method': 'BUS_SERVICE_ENABLE_OR_DISABLE', 'description': 'Bus Service Enable / Disable'}),
    url(r'^bus_service/bus_service_handler/$', 'bus_service_handler'),
)

urlpatterns += patterns('webapp.view.bus_route_view',
    url(r'^bus_route/$', RedirectView.as_view(url='/webapp/bus_route/bus_route_ncs/')),
    url(r'^bus_route/bus_route_ncs/$', 'bus_route_home', {'method': 'BUS_ROUTE_NCS', 'description': 'Bus Route NCS Add / Update'}),
    url(r'^bus_route/bus_route_lta/$', 'bus_route_home', {'method': 'BUS_ROUTE_LTA', 'description': 'Bus Route LTA Add / Update'}),
    url(r'^bus_route/bus_route_handler/$', 'bus_route_handler'),
)

urlpatterns += patterns('webapp.view.sql_view',
    url(r'^sql/$', RedirectView.as_view(url='/webapp/sql/sql_download/')),
    url(r'^sql/sql_download/$', 'sql_home', {'method': 'SQL_DOWNLOAD', 'description': 'SQL Download'}),
    url(r'^sql/sql_delete/$', 'sql_home', {'method': 'SQL_DELETE', 'description': 'SQL Delete'}),
    url(r'^sql/sql_handler/$', 'sql_handler'),
)

urlpatterns += patterns('webapp.view.street_view',
    url(r'^street/street_search/$', 'street_search'),
)