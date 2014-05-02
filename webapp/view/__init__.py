import json
import logging
from django.contrib import messages
from django.http.response import HttpResponse
from django.shortcuts import render
from webapp.exceptions import PTPError

__author__ = 'Gao Lei'

_logger = logging.getLogger('default')


class GlobalHandler(object):

    def __init__(self, func):
        self.func = func

    def __call__(self, *args, **kwargs):
        pass


class GlobalErrorHandler(GlobalHandler):

    def __call__(self, *args, **kwargs):
        try:
            response = self.func(*args, **kwargs)
        except PTPError, ex:
            request = args[0]
            messages.error(request, ex)
            response = render(request, 'common/result.html')
        except Exception, ex:
            request = args[0]
            err_msg = 'Unknown Error: %s' % ex
            messages.error(request, err_msg)
            _logger.error(err_msg)
            response = render(request, 'common/result.html')
        return response


class GlobalAjaxErrorHandler(GlobalHandler):

    def __call__(self, *args, **kwargs):
        try:
            response = self.func(*args, **kwargs)
        except PTPError, ex:
            response_content = json.dumps({'error': str(ex)})
            response = HttpResponse(response_content, content_type='application/json;charset=utf-8')
        except Exception, ex:
            err_msg = 'Unknown Error: %s' % ex
            _logger.error(err_msg)
            response_content = json.dumps({'error': err_msg})
            response = HttpResponse(response_content, content_type='application/json;charset=utf-8')
        return response