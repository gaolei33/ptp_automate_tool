import re

__author__ = 'Gao Lei'

def _wrap_quotes(origin_str):
    target_str = '\'%s\'' % origin_str
    return target_str

def _is_empty(origin_str):
    return origin_str in ('', '-')

class Rule():

    def __init__(self, origin_total_bus_routes):
        self.origin_row_len = 12
        self.origin_total_bus_routes = origin_total_bus_routes
        self.target_total_bus_routes = []

    def _normal_rule(self, origin_str):
        target_str = _wrap_quotes(origin_str)
        return target_str

    def _bus_stop_code_rule(self, origin_bus_stop_code):
        pattern = r'^\d{4}$'
        if re.search(pattern, origin_bus_stop_code):
            offset = '0' * (5 - len(origin_bus_stop_code))
            origin_bus_stop_code = '%s%s' % (offset,  origin_bus_stop_code)
        target_bus_stop_code = self._normal_rule(origin_bus_stop_code)
        return target_bus_stop_code

    def _express_code_and_distance_rule(self, origin_express_code, origin_distance):
        if _is_empty(origin_express_code):
            target_express_code = 'NULL'
            target_distance = self._normal_rule(origin_distance)
        else:
            target_express_code = self._normal_rule(origin_express_code)
            target_distance = 'NULL'
        return (target_express_code, target_distance)

    def execute_rules(self):
        for origin_bus_routes in self.origin_total_bus_routes:

            target_bus_routes = {
                'ID': origin_bus_routes['ID'],
                'DATA': [],
            }

            for origin_row in origin_bus_routes['DATA']:

                if len(origin_row) < self.origin_row_len:
                    raise RuntimeError('Column number must be more than %d!' % self.origin_row_len)

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
                    else:
                        target_str = self._normal_rule(origin_row[i])
                        target_row.append(target_str)

                target_bus_routes['DATA'].append(target_row)

            self.target_total_bus_routes.append(target_bus_routes)

        return self.target_total_bus_routes

