from django.shortcuts import render
from webapp import config
from webapp.view import GlobalErrorHandler

__author__ = 'Gao Lei'


@GlobalErrorHandler
def html_shp_kml_home(request, description):
    return render(request, 'html_shp_kml/html_shp_kml_home.html', {
        'html_shp_kml_real_url': config.HTML_SHP_KML_REAL_URL,
        'description': description,
    })
