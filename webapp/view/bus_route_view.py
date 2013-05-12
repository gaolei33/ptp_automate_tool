from django.contrib import messages
from django.shortcuts import render
from webapp.exceptions import PTPValueError
from webapp.manager import bus_route_manager, csv_manager
from webapp.view import GlobalErrorHandler

__author__ = 'Gao Lei'


@GlobalErrorHandler
def bus_route_home(request, method, description):
    csv_list = csv_manager.get_csv_list(method)
    return render(request, 'bus_route/bus_route_home.html', {
        'method': method,
        'csv_list': csv_list,
        'description': description,
    })


@GlobalErrorHandler
def bus_route_handler(request):
    sr_number = request.POST['sr_number'].strip() or 'Unknown'
    csv_name = request.POST['csv_name'].strip()
    method = request.POST['method'].strip()
    bus_service_ids_string = request.POST['bus_service_ids'].strip()
    bus_service_ids = {item.strip() for item in bus_service_ids_string.split(',') if item.strip()}

    if not bus_service_ids:
        raise PTPValueError('Please input the bus service IDs of which you want to add or update the bus route.')

    if not csv_name:
        raise PTPValueError('Please select a valid bus route CSV file.')

    sql_name = bus_route_manager.bus_route_add_or_update(csv_name, method, bus_service_ids, sr_number)

    messages.info(request, 'SQL generated and executed on development database successfully.')
    request.ATTRIBUTES = {'sql_name': sql_name}

    return render(request, 'common/result.html')