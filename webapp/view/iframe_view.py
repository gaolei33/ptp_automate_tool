from django.shortcuts import render
from webapp.view import GlobalErrorHandler

__author__ = 'Gao Lei'


@GlobalErrorHandler
def iframe_home(request, real_url, description):
    return render(request, 'iframe/iframe_home.html', {
        'real_url': real_url,
        'description': description,
    })
