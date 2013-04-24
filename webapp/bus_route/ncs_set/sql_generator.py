__author__ = 'Gao Lei'

def generate_sql(total_bus_routes):
    sql = ''
    for bus_routes in total_bus_routes:
        sql += "DELETE FROM bus_routes WHERE bus_service_id = %s AND provider = 'NCS';\n" % bus_routes['ID']
        for bus_route in bus_routes['DATA']:
            sql += "INSERT INTO bus_routes (bus_service_id, direction, sequence, bus_stop_id, provider, express_code, distance_fares_marker, distance, weekday_first_trip, weekday_last_trip, saturday_first_trip, saturday_last_trip, sunday_first_trip, sunday_last_trip, note, shows_arrival_table, shows_fare_table, in_operation) VALUES(%s, %s, %s, %s, 'NCS', %s, NULL, %s, %s, %s, %s, %s, %s, %s, NULL, '0', '0', '1');\n" % (bus_route[0], bus_route[1], bus_route[2], bus_route[3], bus_route[4], bus_route[5], bus_route[6], bus_route[7], bus_route[8], bus_route[9], bus_route[10], bus_route[11])
    return sql