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
    url(r'^bus_stop/$', RedirectView.as_view(url='/webapp/bus_stop/bus_stop_add/')),
    url(r'^bus_stop/bus_stop_add/$', 'bus_stop_home', {'method': 'BUS_STOP_ADD'}),
    url(r'^bus_stop/bus_stop_update/$', 'bus_stop_home', {'method': 'BUS_STOP_UPDATE'}),
    url(r'^bus_stop/bus_stop_detail/$', 'bus_stop_detail'),
    url(r'^bus_stop/bus_stop_handler/$', 'bus_stop_handler'),
)

urlpatterns += patterns('webapp.view.bus_service_view',
    url(r'^bus_service/$', RedirectView.as_view(url='/webapp/bus_service/bus_service_add_or_update/')),
    url(r'^bus_service/bus_service_add_or_update/$', 'bus_service_home', {'method': 'BUS_SERVICE_ADD_OR_UPDATE'}),
    url(r'^bus_service/bus_service_enable_or_disable/$', 'bus_service_home', {'method': 'BUS_SERVICE_ENABLE_OR_DISABLE'}),
    url(r'^bus_service/bus_service_handler/$', 'bus_service_handler'),
)

urlpatterns += patterns('webapp.view.bus_route_view',
    url(r'^bus_route/$', RedirectView.as_view(url='/webapp/bus_route/bus_route_ncs/')),
    url(r'^bus_route/bus_route_ncs/$', 'bus_route_home', {'csv_type': 'BUS_ROUTE_NCS'}),
    url(r'^bus_route/bus_route_lta/$', 'bus_route_home', {'csv_type': 'BUS_ROUTE_LTA'}),
    url(r'^bus_route/bus_route_handler/$', 'bus_route_handler'),
)

urlpatterns += patterns('webapp.view.sql_view',
    url(r'^sql/download_sql/$', 'download_sql'),
)

urlpatterns += patterns('webapp.view.street_view',
    url(r'^street/street_search/$', 'street_search'),
)