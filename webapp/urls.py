from django.views.generic.base import RedirectView
from django.conf.urls import patterns, url

__author__ = 'Gao Lei'


urlpatterns = patterns('',
    url(r'^$', RedirectView.as_view(url='/webapp/db/')),
)

urlpatterns += patterns('webapp.view.csv_view',
    url(r'^csv/$', 'csv_home'),
    url(r'^csv/upload_csv/$', 'upload_csv'),
    url(r'^csv/get_csv_list/$', 'get_csv_list'),
)

urlpatterns += patterns('webapp.view.db_view',
    url(r'^db/$', 'db_home'),
    url(r'^db/backup/$', 'db_backup'),
    url(r'^db/restore/$', 'db_restore'),
)

urlpatterns += patterns('webapp.view.bus_stop_view',
    url(r'^bus_stop/$', RedirectView.as_view(url='/webapp/bus_stop/from_csv/')),
    url(r'^bus_stop/from_csv/$', 'bus_stop_home', {'data_source_type': 'CSV'}),
    url(r'^bus_stop/from_db/$', 'bus_stop_home', {'data_source_type': 'DB'}),
    url(r'^bus_stop/bus_stop_detail/$', 'bus_stop_detail'),
    url(r'^bus_stop/generate_bus_stop_sql/$', 'generate_bus_stop_sql'),
    url(r'^bus_stop/street_search/$', 'street_search'),
)

urlpatterns += patterns('webapp.view.bus_route_view',
    url(r'^bus_route/$', RedirectView.as_view(url='/webapp/bus_route/bus_route_ncs/')),
    url(r'^bus_route/bus_route_ncs/$', 'bus_route_home', {'csv_type': 'BUS_ROUTE_NCS'}),
    url(r'^bus_route/bus_route_lta/$', 'bus_route_home', {'csv_type': 'BUS_ROUTE_LTA'}),
    url(r'^bus_route/generate_bus_route_sql/$', 'generate_bus_route_sql'),
)

urlpatterns += patterns('webapp.view.sql_view',
    url(r'^sql/download_sql/$', 'download_sql'),
)