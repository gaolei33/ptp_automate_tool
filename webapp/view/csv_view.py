from django.contrib import messages
from django.shortcuts import render
from webapp.manager import csv_manager

__author__ = 'Gao Lei'


def csv_home(request, method, description):
    csv_list = csv_manager.get_csv_list()
    return render(request, 'csv/csv_home.html', {
        'csv_list': csv_list,
        'method': method,
        'description': description,
    })


def csv_handler(request):
    try:
        method = request.POST['method'].strip()

        if method == 'CSV_UPLOAD':
            csv_file = request.FILES['csv_file']
            csv_type = request.POST['csv_type'].strip()
            sr_number = request.POST['sr_number'].strip() or 'Unknown'

            csv_manager.save_csv(csv_file, csv_type, sr_number)

            messages.info(request, 'CSV file uploaded successfully.')
        else:
            csv_name = request.POST['csv_name'].strip()
            if not csv_name:
                raise ValueError('Please select a valid CSV file to delete.')
            csv_manager.delete(csv_name)
            messages.info(request, 'CSV file deleted successfully.')
    except ValueError, ex:
        messages.error(request, ex)
    except Exception, ex:
        messages.error(request, ex)
    return render(request, 'common/result.html')