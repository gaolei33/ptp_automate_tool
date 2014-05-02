from django.contrib import messages
from django.shortcuts import render
from webapp.exceptions import PTPValueError
from webapp.manager import bus_stop_manager, csv_manager
from webapp.view import GlobalErrorHandler

__author__ = 'Gao Lei'


@GlobalErrorHandler
def bus_stop_home(request, method, description):
    csv_list = csv_manager.get_csv_list('BUS_STOP')
    return render(request, 'bus_stop/bus_stop_home.html', {
        'method': method,
        'csv_list': csv_list,
        'description': description,
    })


@GlobalErrorHandler
def bus_stop_detail(request):
    sr_number = request.POST['sr_number'].strip() or 'Unknown'
    method = request.POST['method'].strip()
    bus_stop_ids_string = request.POST['bus_stop_ids'].strip()
    bus_stop_ids = {item.strip() for item in bus_stop_ids_string.split(',') if item.strip()}

    if not bus_stop_ids:
        raise PTPValueError('Please input the bus stop IDs that you want to add or update.')

    if method == 'BUS_STOP_ADD':

        csv_name = request.POST['csv_name'].strip()
        if not csv_name:
            raise PTPValueError('Please select a valid CSV file.')

        bus_stops = bus_stop_manager.get_bus_stops_from_csv(csv_name, bus_stop_ids)
    else:
        bus_stops = bus_stop_manager.get_bus_stops_from_db(bus_stop_ids)

    return render(request, 'bus_stop/bus_stop_detail.html', {
        'method': method,
        'bus_stops': bus_stops,
        'sr_number': sr_number,
    })


@GlobalErrorHandler
def bus_stop_handler(request):
    method = request.POST['method'].strip()
    sr_number = request.POST['sr_number'].strip() or 'Unknown'
    bus_stop_count = int(request.POST['bus_stop_count'].strip())

    bus_stops = []
    for i in range(bus_stop_count):
        bus_stop_id = request.POST['bus_stop_id_%d' % i].strip()
        street_id = request.POST['street_id_%d' % i].strip()
        long_name = request.POST['long_name_%d' % i].strip()
        short_name = request.POST['short_name_%d' % i].strip()
        location_code = request.POST['location_code_%d' % i].strip() or 'NULL'
        wab_accessible = request.POST['wab_accessible_%d' % i].strip()
        non_bus_stop = request.POST['non_bus_stop_%d' % i].strip()
        interchange = request.POST['interchange_%d' % i].strip()
        longitude = request.POST['longitude_%d' % i].strip()
        latitude = request.POST['latitude_%d' % i].strip()

        bus_stop = [bus_stop_id, street_id, long_name, short_name, location_code, wab_accessible, non_bus_stop, interchange, longitude, latitude]

        bus_stops.append(bus_stop)

    sql_name = bus_stop_manager.bus_stop_add_or_update(bus_stops, sr_number, method)

    messages.info(request, 'SQL generated and executed on development database successfully.')
    request.attributes = {'sql_name': sql_name}

    return render(request, 'common/result.html')