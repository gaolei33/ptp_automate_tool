import logging
from webapp.exceptions import PTPValueError
from webapp.manager import street_manager
from webapp.rule.rule import BaseRule

__author__ = 'Gao Lei'

_logger = logging.getLogger('default')


class BusServiceRule(BaseRule):

    def __init__(self, origin_bus_services):
        BaseRule.__init__(self, 10)
        self.origin_bus_services = origin_bus_services
        self.target_bus_services = []

    def _loop_street_rule(self, origin_loop_street_name):
        if origin_loop_street_name:
            target_loop_street_id = street_manager.get_first_matched_street_id_from_name(origin_loop_street_name)
            if not target_loop_street_id:
                err_msg = 'Cannot find the loop street id for: %s, maybe you uploaded an incorrect CSV file, please check and modify the CSV file.' % origin_loop_street_name
                _logger.error(err_msg)
                raise PTPValueError(err_msg)
        else:
            target_loop_street_id = 'NULL'
        return target_loop_street_id

    def execute_rules(self):

        for origin_bus_service in self.origin_bus_services:

            target_bus_service = []

            for origin_direction in origin_bus_service:
                # column number check
                self._column_number_rule(origin_direction)

                target_direction = []

                for i in range(0, 10):
                    if i == 9:
                        target_loop_street_id = self._loop_street_rule(origin_direction[i])
                        target_direction.append(target_loop_street_id)
                    elif i in (3, 4):
                        #skip 2 columns
                        continue
                    else:
                        target_col = origin_direction[i]
                        target_direction.append(target_col)

                target_bus_service.append(target_direction)

            self.target_bus_services.append(target_bus_service)

        return self.target_bus_services