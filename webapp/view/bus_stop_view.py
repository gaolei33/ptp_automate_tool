import json
from django.contrib import messages
from django.http.response import Http404, HttpResponse
from django.shortcuts import render
from webapp.manager import bus_stop_manager, csv_manager

__author__ = 'Gao Lei'


def bus_stop_home(request, data_source_type):
    csv_list = csv_manager.get_csv_list('BUS_STOP')
    return render(request, 'bus_stop/bus_stop_home.html', {
        'data_source_type': data_source_type,
        'csv_list': csv_list,
    })


def bus_stop_detail(request):
    try:
        data_source_type = request.POST['data_source_type'].strip()
        bus_stop_ids_string = request.POST['bus_stop_ids'].strip()
        bus_stop_ids = {elem.strip() for elem in bus_stop_ids_string.split(',') if elem.strip()}

        if not bus_stop_ids:
            raise ValueError('Please input the bus stop ids that you want to add or update.')

        if data_source_type == 'CSV':

            csv_name = request.POST['csv_name'].strip()
            if not csv_name:
                raise ValueError('Please select a valid bus stop CSV file.')

            total_bus_stop_info = bus_stop_manager.get_bus_stop_info_from_csv(csv_name, bus_stop_ids)
        else:
            total_bus_stop_info = bus_stop_manager.get_bus_stop_info_from_db(bus_stop_ids)
    except KeyError, ex:
        messages.error(request, ex)
        return render(request, 'common/result.html')
    except ValueError, ex:
        messages.error(request, ex)
        return render(request, 'common/result.html')
    return render(request, 'bus_stop/bus_stop_detail.html', {
        'total_bus_stop_info': total_bus_stop_info,
        'bus_stop_ids_string': '_'.join(bus_stop_ids),
    })


def generate_bus_stop_sql(request):
    try:
        total_bus_stop_info = list()

        sr_number = request.POST['sr_number'].strip() or 'Unknown'
        bus_stop_ids_string = request.POST['bus_stop_ids_string'].strip()

        bus_stop_count = int(request.POST['bus_stop_count'].strip())
        for i in range(bus_stop_count):
            bus_stop_id = request.POST['bus_stop_id_%d' % i].strip()
            street_id = request.POST['street_id_%d' % i].strip()
            short_name = request.POST['short_name_%d' % i].strip()
            long_name = request.POST['long_name_%d' % i].strip()
            location_code = request.POST['location_code_%d' % i].strip() or 'NULL'
            wab_accessible = request.POST['wab_accessible_%d' % i].strip()
            non_bus_stop = request.POST['non_bus_stop_%d' % i].strip()
            interchange = request.POST['interchange_%d' % i].strip()

            bus_stop_info = [bus_stop_id, street_id, short_name, long_name, location_code, wab_accessible, non_bus_stop, interchange]

            total_bus_stop_info.append(bus_stop_info)

        bus_stop_manager.bus_stop_update(total_bus_stop_info, sr_number, bus_stop_ids_string)

        messages.info(request, 'SQL generated and executed on development database successfully.')
    except KeyError, ex:
        messages.error(request, ex)
    except ValueError, ex:
        messages.error(request, ex)
    return render(request, 'common/result.html')


def street_search(request):
    try:
        keyword = request.GET['keyword'].strip()
        keyword_type = request.GET['keyword_type'].strip()
        street_list = bus_stop_manager.street_search(keyword, keyword_type)
        street_list_json = json.dumps(street_list)
    except:
        raise Http404
    return HttpResponse(street_list_json, content_type='application/json;charset=utf-8')