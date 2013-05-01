import json
from django.contrib import messages
from django.http.response import HttpResponse, Http404
from django.shortcuts import render
from webapp.manager import csv_manager

__author__ = 'Gao Lei'


def csv_home(request):
    return render(request, 'csv/csv_home.html')


def upload_csv(request):
    try:
        csv_file = request.FILES['csv_file']
        csv_type = request.POST['csv_type'].strip()
        sr_number = request.POST['sr_number'].strip() or 'Unknown'
        csv_manager.save_csv(csv_file, csv_type, sr_number)
        messages.info(request, 'CSV uploaded successfully.')
    except KeyError, ex:
        messages.error(request, ex)
    return render(request, 'common/result.html')


def get_csv_list(request):
    try:
        csv_type = request.GET['csv_type'].strip()
        csv_list = csv_manager.get_csv_list(csv_type)
        csv_list_json = json.dumps(csv_list)
    except:
        raise Http404
    return HttpResponse(csv_list_json, content_type='application/json;charset=utf-8')
