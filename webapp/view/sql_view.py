import logging
from django.http.response import HttpResponse, Http404
from webapp.manager import sql_manager

__author__ = 'Gao Lei'

_logger = logging.getLogger('default')


def download_sql(request):
    try:
        sql_name = request.GET['sql_name'].strip()
        sql_file = sql_manager.get_sql(sql_name)
        response = HttpResponse(sql_file, content_type='text/plain')
        response['Content-Disposition'] = 'attachment; filename="%s"' % sql_name
    except KeyError, ex:
        err_msg = 'An error occurred while downloading SQL file: %s' % ex
        _logger.error(err_msg)
        raise Http404
    except ValueError, ex:
        err_msg = 'An error occurred while downloading SQL file: %s' % ex
        _logger.error(err_msg)
        raise Http404
    return response