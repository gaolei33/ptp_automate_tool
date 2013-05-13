import json
from django.http.response import HttpResponse
from webapp.manager import street_manager
from webapp.view import GlobalAjaxErrorHandler

__author__ = 'Gao Lei'


@GlobalAjaxErrorHandler
def street_search(request):
    keyword = request.GET['keyword'].strip()
    keyword_type = request.GET['keyword_type'].strip()
    street_list = street_manager.street_search(keyword, keyword_type)
    street_list_json = json.dumps({'streets': street_list})

    return HttpResponse(street_list_json, content_type='application/json;charset=utf-8')