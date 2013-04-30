from django.views.generic.base import RedirectView
from django.conf.urls import patterns, url

__author__ = 'Gao Lei'


urlpatterns = patterns('webapp.views',
    url(r'^$', RedirectView.as_view(url='/webapp/db/')),

    url(r'^csv/$', 'csv_home'),
    url(r'^csv/upload_csv/$', 'upload_csv'),

    url(r'^download_sql/$', 'download_sql'),

    url(r'^get_csv_list/$', 'get_csv_list'),

    url(r'^db/$', 'db_home'),
    url(r'^db/backup/$', 'db_backup'),
    url(r'^db/restore/$', 'db_restore'),

    url(r'^bus_route/$', 'bus_route_home'),
    url(r'^bus_route/generate_bus_route_sql/$', 'generate_bus_route_sql'),

    url(r'^bus_stop/$', 'bus_stop_home'),
    url(r'^bus_stop/bus_stop_detail/$', 'bus_stop_detail'),
    url(r'^bus_stop/generate_bus_stop_sql/$', 'generate_bus_stop_sql'),

    url(r'^street_search/$', 'street_search'),
)