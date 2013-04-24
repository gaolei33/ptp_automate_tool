# Create your views here.
import logging
from django.contrib import messages
from django.http.response import HttpResponse, Http404
from django.shortcuts import render
from webapp import config
from webapp.bus_route import bus_route_manager
from webapp.common.io import csv_manager, sql_manager
from webapp.db import db_manager

_logger = logging.getLogger('default')

def upload_csv(request):

    try:
        csv_file = request.FILES['csv_file']
        sr_number = request.POST['sr_number'] or 'Unknown'
        csv_manager.save_csv(csv_file, config.BUS_ROUTE_NCS, sr_number)
        messages.info(request, 'CSV uploaded successfully.')
    except KeyError, ex:
        messages.error(request, ex)

    return render(request, 'common/result.html')


def download_sql(request):

    try:
        sql_name = request.GET['sql_name']
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


def db_home(request):

    backup_list = db_manager.get_backup_list()

    return render(request, 'db/db_home.html', {
        'backup_list': backup_list,
    })


def db_backup(request):

    try:
        sr_number = request.POST['sr_number'] or 'Unknown'
        db_manager.backup(sr_number)

        messages.info(request, 'Development Database backed up successfully.')
    except KeyError, ex:
        messages.error(request, ex)
    except ValueError, ex:
        messages.error(request, ex)

    return render(request, 'common/result.html')


def db_restore(request):

    try:
        backup_name = request.POST['backup_name']
        db_manager.restore(backup_name)

        messages.info(request, 'Development database restored successfully.')
    except KeyError, ex:
        messages.error(request, ex)
    except ValueError, ex:
        messages.error(request, ex)

    return render(request, 'common/result.html')


def bus_route_home(request):

    csv_list = csv_manager.get_csv_list(config.BUS_ROUTE_NCS)

    return render(request, 'bus_route/bus_route_home.html', {
        'csv_list': csv_list,
    })


def generate_sql(request):

    try:
        csv_name = request.POST['csv_name']
        bus_service_ids_string = request.POST['bus_service_ids']
        bus_service_ids = { elem.strip() for elem in bus_service_ids_string.split(',') if elem.strip() }

        bus_route_manager.bus_route_update(csv_name, config.BUS_ROUTE_NCS, bus_service_ids)

        messages.info(request, 'SQL generated and executed on development database successfully.')
    except KeyError, ex:
        messages.error(request, ex)
    except ValueError, ex:
        messages.error(request, ex)

    return render(request, 'common/result.html')