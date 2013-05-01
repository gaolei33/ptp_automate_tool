import json
from django.http.response import Http404, HttpResponse
from webapp.manager import street_manager

__author__ = 'Gao Lei'


def street_search(request):
    try:
        keyword = request.GET['keyword'].strip()
        keyword_type = request.GET['keyword_type'].strip()
        street_list = street_manager.street_search(keyword, keyword_type)
        street_list_json = json.dumps(street_list)
    except:
        raise Http404
    return HttpResponse(street_list_json, content_type='application/json;charset=utf-8')