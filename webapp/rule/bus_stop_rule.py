import logging
from webapp import config
from webapp.dao import street_dao
from webapp.exceptions import PTPValueError
from webapp.rule.rule import CsvRule

__author__ = 'Gao Lei'

_logger = logging.getLogger('default')


class BusStopRule(CsvRule):

    def __init__(self, origin_bus_stops):
        CsvRule.__init__(self, 3)
        self.origin_bus_stops = origin_bus_stops
        self.target_bus_stops = []

    def _street_id_rule(self, origin_street_name):
        target_street_id = street_dao.get_first_matched_street_id_by_name(origin_street_name)
        if not target_street_id:
            err_msg = 'Cannot find the street id for: %s, maybe you uploaded an incorrect CSV file, please check and modify the CSV file.' % origin_street_name
            _logger.error(err_msg)
            raise PTPValueError(err_msg)
        return target_street_id

    def _long_name_rule(self, origin_short_name):
        target_words = []
        origin_words = origin_short_name.split(' ')
        for origin_word in origin_words:
            origin_word_lower = origin_word.lower()
            target_word = config.BUS_STOP_SHORT_NAME_LONG_NAME_MAP[origin_word_lower] if origin_word_lower in config.BUS_STOP_SHORT_NAME_LONG_NAME_MAP else origin_word
            target_words.append(target_word)
        target_long_name = ' '.join(target_words)
        return target_long_name

    def _non_bus_stop_and_wab_rule(self, origin_bus_stop_id):
        if origin_bus_stop_id.lower().startswith('e'):
            target_wab_accessible = '0'
            target_non_bus_stop = '1'
        else:
            target_wab_accessible = '1'
            target_non_bus_stop = '0'
        return target_wab_accessible, target_non_bus_stop

    def execute_rules(self):

        for origin_bus_stop in self.origin_bus_stops:
            # column number check
            self._column_number_rule(origin_bus_stop)

            target_bus_stop = []

            target_bus_stop_id = origin_bus_stop[0]
            target_bus_stop.append(target_bus_stop_id)

            target_street_id = self._street_id_rule(origin_bus_stop[1])
            target_bus_stop.append(target_street_id)

            target_long_name = self._long_name_rule(origin_bus_stop[2])
            target_bus_stop.append(target_long_name)

            target_short_name = origin_bus_stop[2]
            target_bus_stop.append(target_short_name)

            target_location_code = ''
            target_bus_stop.append(target_location_code)

            target_wab_accessible, target_non_bus_stop = self._non_bus_stop_and_wab_rule(target_bus_stop_id)
            target_bus_stop.append(target_wab_accessible)
            target_bus_stop.append(target_non_bus_stop)

            target_interchange = '0'
            target_bus_stop.append(target_interchange)

            target_longitude = '0.00000000000000'
            target_bus_stop.append(target_longitude)

            target_latitude = '0.00000000000000'
            target_bus_stop.append(target_latitude)

            self.target_bus_stops.append(target_bus_stop)

        return self.target_bus_stops