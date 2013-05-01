from django.contrib import messages
from django.shortcuts import render
from webapp.manager import bus_route_manager, csv_manager

__author__ = 'Gao Lei'


def bus_route_home(request, csv_type):
    csv_list = csv_manager.get_csv_list(csv_type)
    return render(request, 'bus_route/bus_route_home.html', {
        'csv_type': csv_type,
        'csv_list': csv_list,
    })


def generate_bus_route_sql(request):
    try:
        sr_number = request.POST['sr_number'].strip() or 'Unknown'
        csv_name = request.POST['csv_name'].strip()
        csv_type = request.POST['csv_type'].strip()
        bus_service_ids_string = request.POST['bus_service_ids'].strip()
        bus_service_ids = {elem.strip() for elem in bus_service_ids_string.split(',') if elem.strip()}

        if not bus_service_ids:
            raise ValueError('Please input the bus service ids of which you want to add or update the bus route.')

        if not csv_name:
            raise ValueError('Please select a valid bus route CSV file.')

        bus_route_manager.bus_route_update(csv_name, csv_type, bus_service_ids, sr_number)

        messages.info(request, 'SQL generated and executed on development database successfully.')
    except KeyError, ex:
        messages.error(request, ex)
    except ValueError, ex:
        messages.error(request, ex)
    return render(request, 'common/result.html')