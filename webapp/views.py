# Create your views here.
import json
import logging
from django.contrib import messages
from django.http.response import HttpResponse, Http404
from django.shortcuts import render
from webapp.manager import bus_route_manager, db_manager, csv_manager, bus_stop_manager, sql_manager

_logger = logging.getLogger('default')


def csv_home(request):
    return render(request, 'csv/csv_home.html')


def upload_csv(request):
    try:
        csv_file = request.FILES['csv_file']
        csv_type = request.POST['csv_type']
        sr_number = request.POST['sr_number'] or 'Unknown'
        csv_manager.save_csv(csv_file, csv_type, sr_number)
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
    return render(request, 'bus_route/bus_route_home.html', {
        'csv_types': (
            'BUS_ROUTE_NCS',
            'BUS_ROUTE_LTA',
        )
    })


def generate_bus_route_sql(request):
    try:
        csv_name = request.POST['csv_name']
        csv_type = request.POST['csv_type']
        bus_service_ids_string = request.POST['bus_service_ids']
        bus_service_ids = { elem.strip() for elem in bus_service_ids_string.split(',') if elem.strip() }

        bus_route_manager.bus_route_update(csv_name, csv_type, bus_service_ids)

        messages.info(request, 'SQL generated and executed on development database successfully.')
    except KeyError, ex:
        messages.error(request, ex)
    except ValueError, ex:
        messages.error(request, ex)
    return render(request, 'common/result.html')


def get_csv_list(request):
    try:
        csv_type = request.GET['csv_type']
        csv_list = csv_manager.get_csv_list(csv_type)
        csv_list_json = json.dumps(csv_list)
    except:
        raise Http404
    return HttpResponse(csv_list_json, content_type='application/json;charset=utf-8')


def bus_stop_home(request):
    return render(request, 'bus_stop/bus_stop_home.html', {
        'csv_types': (
            'BUS_STOP',
        )
    })


def bus_stop_detail(request):
    try:
        csv_name = request.POST['csv_name']
        bus_stop_ids_string = request.POST['bus_stop_ids']
        bus_stop_ids = { elem.strip() for elem in bus_stop_ids_string.split(',') if elem.strip() }

        total_bus_stop_info = bus_stop_manager.get_bus_stop_info(csv_name, bus_stop_ids)
    except KeyError, ex:
        messages.error(request, ex)
        return render(request, 'common/result.html')
    except ValueError, ex:
        messages.error(request, ex)
        return render(request, 'common/result.html')
    return render(request, 'bus_stop/bus_stop_detail.html', {
        'total_bus_stop_info': total_bus_stop_info,
        'csv_name': csv_name,
        'bus_stop_ids_string': '_'.join(bus_stop_ids),
    })


def generate_bus_stop_sql(request):
    try:
        total_bus_stop_info = list()

        csv_name = request.POST['csv_name']
        bus_stop_ids_string = request.POST['bus_stop_ids_string']

        bus_stop_count = int(request.POST['bus_stop_count'])
        for i in range(bus_stop_count):
            bus_stop_id = request.POST['bus_stop_id_%d' % i].strip()
            street_id = request.POST['street_id_%d' % i].strip()
            short_name = request.POST['short_name_%d' % i].strip()
            long_name = request.POST['long_name_%d' % i].strip()
            location_code = request.POST['location_code_%d' % i].strip() or 'NULL'
            wab_accessible = request.POST['wab_accessible_%d' % i].strip()
            express = request.POST['express_%d' % i].strip()

            bus_stop_info = [bus_stop_id, street_id, short_name, long_name, location_code, wab_accessible, express]

            total_bus_stop_info.append(bus_stop_info)

        bus_stop_manager.bus_stop_update(total_bus_stop_info, csv_name, bus_stop_ids_string)

        messages.info(request, 'SQL generated and executed on development database successfully.')
    except KeyError, ex:
        messages.error(request, ex)
    except ValueError, ex:
        messages.error(request, ex)
    return render(request, 'common/result.html')


def street_search(request):
    try:
        keyword = request.GET['keyword']
        keyword_type = request.GET['keyword_type']
        street_list = bus_stop_manager.street_search(keyword, keyword_type)
        street_list_json = json.dumps(street_list)
    except:
        raise Http404
    return HttpResponse(street_list_json, content_type='application/json;charset=utf-8')