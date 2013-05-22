from webapp.manager import csv_manager, sql_manager
from webapp.rule.taxi_rule import TaxiPostRule, TaxiPostTimingRule
from webapp.util import string_util, db_util

__author__ = 'Gao Lei'


def taxi_post_or_post_timing_add(csv_name, method):
    taxi_post_or_post_timing = csv_manager.retrieve_data_from_csv(csv_name, method)

    rule = TaxiPostRule(taxi_post_or_post_timing) if method == 'TAXI_POST' else TaxiPostTimingRule(taxi_post_or_post_timing)
    taxi_post_or_post_timing_after_rules = rule.execute_rules()

    taxi_post_or_post_timing_wrap_quotes = string_util.wrap_quotes_except_null(taxi_post_or_post_timing_after_rules)

    # generate SQL string
    sql = generate_sql(taxi_post_or_post_timing_wrap_quotes, method)

    # execute the generated SQL on development database
    db_util.exec_cmds(sql, 'TAXI')

    # save SQL string to file
    sql_name = sql_manager.get_sql_name('Unknown', method, 'ALL')
    sql_manager.save_sql(sql_name, sql)

    return sql_name


def generate_sql(taxi_post_or_post_timing, method):
    sql = ''
    for taxi_post_or_post_timing in taxi_post_or_post_timing:
        if method == 'TAXI_POST':
            sql += "INSERT INTO post (id, nric, name, phoneNumber, email, streetName, mode, matchStatus, taxiCompanyId, vehicleType, vehicleModelId, status, createdDate, lastUpdatedDate) VALUES (%s, %s, %s, %s, %s, %s, %s, '0', %s, %s, %s, 'A', NOW(), NOW());\n" % (taxi_post_or_post_timing[0], taxi_post_or_post_timing[1], taxi_post_or_post_timing[2], taxi_post_or_post_timing[3], taxi_post_or_post_timing[4], taxi_post_or_post_timing[5], taxi_post_or_post_timing[6], taxi_post_or_post_timing[7], taxi_post_or_post_timing[8], taxi_post_or_post_timing[9])
        else:
            sql += "INSERT INTO post_timing (postId, dayId, startTime, endTime) VALUES (%s, %s, %s, %s);\n" % (taxi_post_or_post_timing[0], taxi_post_or_post_timing[1], taxi_post_or_post_timing[2], taxi_post_or_post_timing[3])
    return sql