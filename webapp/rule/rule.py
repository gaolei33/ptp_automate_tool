import logging
from webapp.exceptions import PTPValueError

__author__ = 'Gao Lei'

_logger = logging.getLogger('default')


class BaseRule():

    def __init__(self, column_number):
        self.column_number = column_number

    def _column_number_rule(self, origin_row):
        if len(origin_row) < self.column_number:
            err_msg = 'CSV columns must be more than %d, maybe you uploaded an incorrect CSV file, please check and modify the CSV file.' % self.column_number
            _logger.error(err_msg)
            raise PTPValueError(err_msg)

    def execute_rules(self):
        pass