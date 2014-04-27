from django.contrib import messages
from django.shortcuts import render
from webapp.exceptions import PTPValueError
from webapp.manager import bus_route_manager, csv_manager
from webapp.view import GlobalErrorHandler

__author__ = 'Gao Lei'


@GlobalErrorHandler
def bus_route_home(request, method, description):
    csv_list_ncs = csv_manager.get_csv_list('BUS_ROUTE_NCS')
    csv_list_lta = csv_manager.get_csv_list('BUS_ROUTE_LTA')
    return render(request, 'bus_route/bus_route_home.html', {
        'method': method,
        'csv_list_ncs': csv_list_ncs,
        'csv_list_lta': csv_list_lta,
        'description': description,
    })


@GlobalErrorHandler
def bus_route_handler(request):
    sr_number = request.POST['sr_number'].strip() or 'Unknown'
    csv_name_ncs = request.POST['csv_name_ncs'].strip()
    csv_name_lta = request.POST['csv_name_lta'].strip()
    bus_service_ids_string = request.POST['bus_service_ids'].strip()
    bus_service_ids = {item.strip() for item in bus_service_ids_string.split(',') if item.strip()}

    if not bus_service_ids:
        raise PTPValueError('Please input the bus service IDs of which you want to add or update the bus route.')

    if not csv_name_ncs:
        raise PTPValueError('Please select a valid CSV file for NCS set.')

    if not csv_name_lta:
        raise PTPValueError('Please select a valid CSV file for LTA set.')

    sql_name = bus_route_manager.bus_route_add_or_update(csv_name_ncs, csv_name_lta, bus_service_ids, sr_number)

    messages.info(request, 'SQL generated and executed on development database successfully.')
    request.ATTRIBUTES = {'sql_name': sql_name}

    return render(request, 'common/result.html')