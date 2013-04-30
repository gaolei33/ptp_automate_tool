import logging
import re
from webapp.rule.rule import BaseRule

__author__ = 'Gao Lei'

_logger = logging.getLogger('default')


def _is_empty(origin_str):
    return origin_str in ('', '-')


class BusRouteRule(BaseRule):

    def __init__(self, origin_total_bus_routes, origin_row_len):
        self.origin_row_len = origin_row_len
        self.origin_total_bus_routes = origin_total_bus_routes
        self.target_total_bus_routes = []

    def _bus_stop_code_rule(self, origin_bus_stop_code):
        pattern = r'^\d{4}$'
        if re.search(pattern, origin_bus_stop_code):
            offset = '0' * (5 - len(origin_bus_stop_code))
            origin_bus_stop_code = '%s%s' % (offset,  origin_bus_stop_code)
        target_bus_stop_code = self._normal_rule(origin_bus_stop_code)
        return target_bus_stop_code


class BusRouteNCSRule(BusRouteRule):

    def __init__(self, origin_total_bus_routes):
        BusRouteRule.__init__(self, origin_total_bus_routes, 12)

    def _express_code_and_distance_rule(self, origin_express_code, origin_distance):
        if _is_empty(origin_express_code):
            target_express_code = 'NULL'
            target_distance = self._normal_rule(origin_distance)
        else:
            target_express_code = self._normal_rule(origin_express_code)
            target_distance = 'NULL'
        return (target_express_code, target_distance)

    def _trip_rule(self, origin_trip):
        if _is_empty(origin_trip):
            origin_trip = '-'
        else:
            offset = '0' * (4 - len(origin_trip))
            origin_trip = '%s%s' % (offset,  origin_trip)
        target_trip = self._normal_rule(origin_trip)
        return target_trip

    def execute_rules(self):
        for origin_bus_routes in self.origin_total_bus_routes:

            target_bus_routes = {
                'ID': origin_bus_routes['ID'],
                'DATA': [],
            }

            for origin_row in origin_bus_routes['DATA']:

                if len(origin_row) < self.origin_row_len:
                    err_msg = 'CSV columns must be more than %d!' % self.origin_row_len
                    _logger.error(err_msg)
                    raise ValueError(err_msg)

                target_row = []

                for i in range(0, self.origin_row_len):
                    if i == 3:
                        target_bus_stop_code = self._bus_stop_code_rule(origin_row[i])
                        target_row.append(target_bus_stop_code)
                    elif i == 4:
                        target_express_code, target_distance = self._express_code_and_distance_rule(origin_row[4], origin_row[5])
                        target_row.append(target_express_code)
                        target_row.append(target_distance)
                    elif i == 5:
                        #skip 1 column
                        continue
                    elif i in range(6, 12):
                        target_str = self._trip_rule(origin_row[i])
                        target_row.append(target_str)
                    else:
                        target_str = self._normal_rule(origin_row[i])
                        target_row.append(target_str)

                target_bus_routes['DATA'].append(target_row)

            self.target_total_bus_routes.append(target_bus_routes)

        return self.target_total_bus_routes


class BusRouteLTARule(BusRouteRule):

    def __init__(self, origin_total_bus_routes):
        BusRouteRule.__init__(self, origin_total_bus_routes, 7)

    def _express_code_and_distance_and_fare_marker_rule(self, origin_express_code, origin_distance, origin_fare_marker):
        if _is_empty(origin_express_code):
            target_express_code = 'NULL'
            target_distance = self._normal_rule(origin_distance)
            target_fare_marker = self._fare_marker_rule(origin_fare_marker)
        else:
            target_express_code = self._normal_rule(origin_express_code)
            target_distance = 'NULL'
            target_fare_marker = 'NULL'
        return (target_express_code, target_distance, target_fare_marker)

    def _fare_marker_rule(self, origin_fare_marker):
        if origin_fare_marker in ('', '0'):
            target_fare_marker = 'NULL'
        else:
            target_fare_marker = self._normal_rule(origin_fare_marker)
        return target_fare_marker

    def execute_rules(self):

        for origin_bus_routes in self.origin_total_bus_routes:

            target_bus_routes = {
                'ID': origin_bus_routes['ID'],
                'DATA': [],
            }

            for origin_row in origin_bus_routes['DATA']:

                if len(origin_row) < self.origin_row_len:
                    err_msg = 'CSV columns must be more than %d!' % self.origin_row_len
                    _logger.error(err_msg)
                    raise ValueError(err_msg)

                target_row = []

                for i in range(0, self.origin_row_len):

                    if i == 3:
                        target_bus_stop_code = self._bus_stop_code_rule(origin_row[i])
                        target_row.append(target_bus_stop_code)
                    elif i == 4:
                        target_express_code, target_distance, target_fare_marker = self._express_code_and_distance_and_fare_marker_rule(origin_row[4], origin_row[5], origin_row[6])
                        target_row.append(target_express_code)
                        target_row.append(target_distance)
                        target_row.append(target_fare_marker)
                    elif i == 5 or i == 6:
                        #skip 2 column
                        continue
                    else:
                        target_str = self._normal_rule(origin_row[i])
                        target_row.append(target_str)

                target_bus_routes['DATA'].append(target_row)

            self.target_total_bus_routes.append(target_bus_routes)

        return self.target_total_bus_routes