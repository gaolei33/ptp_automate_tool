from django.contrib import messages
from django.shortcuts import render
from webapp.exceptions import PTPValueError
from webapp.manager import address_manager
from webapp.view import GlobalErrorHandler

__author__ = 'Gao Lei'


@GlobalErrorHandler
def address_home(request, method, description):
    return render(request, 'address/address_home.html', {
        'method': method,
        'description': description,
    })


@GlobalErrorHandler
def address_detail(request):
    postal_codes_string = request.POST['postal_codes'].strip()
    postal_codes = {item.strip() for item in postal_codes_string.split(',') if item.strip()}

    if not postal_codes:
        raise PTPValueError('Please input the bus postal codes that you want to add.')

    address_manager.postal_code_existing_check(postal_codes)

    return render(request, 'address/address_detail.html', {
        'postal_codes': postal_codes,
    })


@GlobalErrorHandler
def address_handler(request):
    address_count = int(request.POST['address_count'].strip())

    addresses = []
    for i in range(address_count):
        postal_code = request.POST['postal_code_%d' % i].strip()
        block = request.POST['block_%d' % i].strip()
        street_name = request.POST['street_name_%d' % i].strip()
        longitude = request.POST['longitude_%d' % i].strip()
        latitude = request.POST['latitude_%d' % i].strip()

        address = [postal_code, block, street_name, longitude, latitude]

        addresses.append(address)

    sql_name = address_manager.address_add(addresses)

    messages.info(request, 'SQL generated and executed on development database successfully.')
    request.attributes = {'sql_name': sql_name}

    return render(request, 'common/result.html')