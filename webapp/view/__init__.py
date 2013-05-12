import logging
from django.contrib import messages
from django.shortcuts import render
from webapp.exceptions import PTPError

__author__ = 'Gao Lei'

_logger = logging.getLogger('default')


class GlobalErrorHandler():

    def __init__(self, func):
        self.func = func

    def __call__(self, *args, **kwargs):
        try:
            response = self.func(*args, **kwargs)
        except PTPError, ex:
            request = args[0]
            messages.error(request, ex)
            return render(request, 'common/result.html')
        except Exception, ex:
            request = args[0]
            err_msg = 'Unknown Error: %s' % ex
            messages.error(request, err_msg)
            _logger.error(err_msg)
            return render(request, 'common/result.html')
        return response