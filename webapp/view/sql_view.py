import logging
from django.contrib import messages
from django.http.response import HttpResponse
from django.shortcuts import render
from webapp.manager import sql_manager
from webapp.view import GlobalErrorHandler

__author__ = 'Gao Lei'

_logger = logging.getLogger('default')


@GlobalErrorHandler
def sql_home(request, method, description):
    sql_list = sql_manager.get_sql_list()
    return render(request, 'sql/sql_home.html', {
        'sql_list': sql_list,
        'method': method,
        'description': description,
    })


@GlobalErrorHandler
def sql_handler(request):
    method = request.GET['method'].strip() if 'method' in request.GET else request.POST['method'].strip()

    if method == 'SQL_DOWNLOAD':
        sql_name = request.GET['sql_name'].strip()
        sql_file = sql_manager.get_sql(sql_name)
        response = HttpResponse(sql_file, content_type='text/plain')
        response['Content-Disposition'] = 'attachment; filename="%s"' % sql_name

        return response
    else:
        sql_name = request.POST['sql_name'].strip()
        sql_manager.delete(sql_name)
        messages.info(request, 'SQL file deleted successfully.')

    return render(request, 'common/result.html')