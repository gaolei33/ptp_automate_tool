from django.http.response import HttpResponse
from django.shortcuts import render
from webapp.manager import pdf_manager
from webapp.view import GlobalErrorHandler

__author__ = 'Gao Lei'


@GlobalErrorHandler
def pdf_home(request, method, description):
    return render(request, 'pdf/pdf_home.html', {
        'method': method,
        'description': description,
    })


@GlobalErrorHandler
def pdf_handler(request):
    pdf_zip_file = request.FILES['pdf_zip_file']
    pdf_content_target = pdf_manager.pdf_rename(pdf_zip_file)
    response = HttpResponse(pdf_content_target, content_type='application/zip')
    response['Content-Disposition'] = 'attachment; filename="pdf.zip"'

    return response