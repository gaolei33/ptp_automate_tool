import logging
from webapp.exceptions import PTPValueError
from webapp.manager import street_manager
from webapp.rule.rule import BaseRule

__author__ = 'Gao Lei'

_logger = logging.getLogger('default')


class TaxiPostRule(BaseRule):

    def __init__(self, origin_taxi_posts):
        BaseRule.__init__(self, 10)
        self.origin_taxi_posts = origin_taxi_posts
        self.target_taxi_posts = []

    def _street_name_rule(self, origin_postal_code):
        if origin_postal_code:
            target_street_name = street_manager.get_street_name_from_postal_code(origin_postal_code)
            if not target_street_name:
                err_msg = 'Cannot find the loop street name for postal code : %s, maybe you uploaded an incorrect CSV file, please check and modify the CSV file.' % origin_postal_code
                _logger.error(err_msg)
                raise PTPValueError(err_msg)
        else:
            target_street_name = ''
        return target_street_name

    def execute_rules(self):

        for origin_taxi_post in self.origin_taxi_posts:
            # column number check
            self._column_number_rule(origin_taxi_post)

            target_taxi_post = []

            for i in range(len(origin_taxi_post)):
                if i == 5:
                    target_street_name = self._street_name_rule(origin_taxi_post[i])
                    target_taxi_post.append(target_street_name)
                else:
                    target_col = origin_taxi_post[i]
                    target_taxi_post.append(target_col)

            self.target_taxi_posts.append(target_taxi_post)

        return self.target_taxi_posts


class TaxiPostTimingRule(BaseRule):

    def __init__(self, origin_taxi_post_timings):
        BaseRule.__init__(self, 4)
        self.origin_taxi_post_timings = origin_taxi_post_timings
        self.target_taxi_post_timings = []

    def execute_rules(self):

        for origin_taxi_post_timing in self.origin_taxi_post_timings:
            # column number check
            self._column_number_rule(origin_taxi_post_timing)

            target_taxi_post_timing = []

            for i in range(len(origin_taxi_post_timing)):
                target_col = origin_taxi_post_timing[i]
                target_taxi_post_timing.append(target_col)

            self.target_taxi_post_timings.append(target_taxi_post_timing)

        return self.target_taxi_post_timings