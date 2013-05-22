from django.contrib import messages
from django.shortcuts import render
from webapp.exceptions import PTPValueError
from webapp.manager import csv_manager, bus_service_manager
from webapp.view import GlobalErrorHandler

__author__ = 'Gao Lei'


@GlobalErrorHandler
def bus_service_home(request, method, description):
    csv_list = csv_manager.get_csv_list('BUS_SERVICE')
    return render(request, 'bus_service/bus_service_home.html', {
        'method': method,
        'csv_list': csv_list,
        'description': description,
    })


@GlobalErrorHandler
def bus_service_handler(request):
    sr_number = request.POST['sr_number'].strip() or 'Unknown'
    method = request.POST['method'].strip()
    bus_service_ids_string = request.POST['bus_service_ids'].strip()
    bus_service_ids = {item.strip() for item in bus_service_ids_string.split(',') if item.strip()}

    if not bus_service_ids:
        raise PTPValueError('Please input the bus service IDs that you want to add or update.')

    if method == 'BUS_SERVICE_ADD_OR_UPDATE':
        csv_name = request.POST['csv_name'].strip()
        if not csv_name:
            raise PTPValueError('Please select a valid CSV file.')
        sql_name = bus_service_manager.bus_service_add_or_update(csv_name, bus_service_ids, sr_number)
    else:
        enable_or_disable = request.POST['enable_or_disable'].strip()
        sql_name = bus_service_manager.bus_service_enable_or_disable(bus_service_ids, enable_or_disable, sr_number)

    messages.info(request, 'SQL generated and executed on development database successfully.')
    request.ATTRIBUTES = {'sql_name': sql_name}

    return render(request, 'common/result.html')