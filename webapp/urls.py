from django.views.generic.base import RedirectView

__author__ = 'Gao Lei'

from django.conf.urls import patterns, url

urlpatterns = patterns('webapp.views',
    url(r'^$', RedirectView.as_view(url='/webapp/db/')),

    url(r'^upload_csv/$', 'upload_csv'),
    url(r'^download_sql/$', 'download_sql'),

    url(r'^db/$', 'db_home'),
    url(r'^db/backup/$', 'db_backup'),
    url(r'^db/restore/$', 'db_restore'),

    url(r'^bus_route/$', 'bus_route_home'),
    url(r'^bus_route/generate_sql/$', 'generate_sql'),
)