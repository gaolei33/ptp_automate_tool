import logging
from webapp.rule.rule import BaseRule

__author__ = 'Gao Lei'

_logger = logging.getLogger('default')

class BusStopRule(BaseRule):

    def __init__(self, origin_total_bus_stop_info):
        self.origin_row_len = 3
        self.origin_total_bus_stop_info = origin_total_bus_stop_info
        self.target_total_bus_stop_info = []

    def _express_and_wab_rule(self, origin_bus_stop_id):
        if origin_bus_stop_id.lower().startswith('e'):
            target_wab_accessible = '0'
            target_express = '1'
        else:
            target_wab_accessible = '1'
            target_express = '0'
        return target_wab_accessible, target_express

    def execute_rules(self):

        for origin_bus_stop_info in self.origin_total_bus_stop_info:

            origin_row = origin_bus_stop_info['DATA'][0]

            if len(origin_row) < self.origin_row_len:
                err_msg = 'CSV columns must be more than %d!' % self.origin_row_len
                _logger.error(err_msg)
                raise ValueError(err_msg)

            target_bus_stop_info = []

            target_bus_stop_id = self._normal_rule(origin_row[0])
            target_bus_stop_info.append(target_bus_stop_id)

            target_street_id = self._normal_rule(origin_row[1])
            target_bus_stop_info.append(target_street_id)

            target_short_name = self._normal_rule(origin_row[2])
            target_bus_stop_info.append(target_short_name)

            target_wab_accessible, target_express = self._express_and_wab_rule(target_bus_stop_id)
            target_bus_stop_info.append(target_wab_accessible)
            target_bus_stop_info.append(target_express)

            self.target_total_bus_stop_info.append(target_bus_stop_info)

        return self.target_total_bus_stop_info

