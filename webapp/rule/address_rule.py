import logging
from webapp.dao import street_dao
from webapp.exceptions import PTPValueError
from webapp.rule.rule import BaseRule

__author__ = 'Gao Lei'

_logger = logging.getLogger('default')


class AddressRule(BaseRule):

    def __init__(self, origin_addresses):
        self.origin_addresses = origin_addresses
        self.target_addresses = []

    def _street_id_rule(self, origin_street_name):
        target_street_id = street_dao.get_first_matched_street_id_by_name(origin_street_name)
        if not target_street_id:
            err_msg = 'Cannot find the street id for: %s, please input correctly.' % origin_street_name
            _logger.error(err_msg)
            raise PTPValueError(err_msg)
        return target_street_id

    def execute_rules(self):
        for origin_address in self.origin_addresses:
            target_address = []
            for i in range(0, 5):
                if i == 2:
                    target_street_id = self._street_id_rule(origin_address[i])
                    target_address.append(target_street_id)
                else:
                    target_col = origin_address[i]
                    target_address.append(target_col)
            self.target_addresses.append(target_address)

        return self.target_addresses