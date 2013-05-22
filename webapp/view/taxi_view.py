from django.contrib import messages
from django.shortcuts import render
from webapp.exceptions import PTPValueError
from webapp.manager import taxi_manager, csv_manager
from webapp.view import GlobalErrorHandler

__author__ = 'Gao Lei'


@GlobalErrorHandler
def taxi_home(request, method, description):
    csv_list = csv_manager.get_csv_list(method)
    return render(request, 'taxi/taxi_home.html', {
        'method': method,
        'csv_list': csv_list,
        'description': description,
    })


@GlobalErrorHandler
def taxi_handler(request):
    csv_name = request.POST['csv_name'].strip()
    method = request.POST['method'].strip()

    if not csv_name:
        raise PTPValueError('Please select a valid CSV file.')

    sql_name = taxi_manager.taxi_post_or_post_timing_add(csv_name, method)

    messages.info(request, 'SQL generated and executed on development database successfully.')
    request.ATTRIBUTES = {'sql_name': sql_name}

    return render(request, 'common/result.html')