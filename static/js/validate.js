/**
 * User: Gao Lei
 * Date: 5/7/13
 * Time: 1:38 AM
 */


$(function() {
    $('#db_form').validate({
        rules: {
            sr_number: {
                required: true,
                digits: true
            },
            backup_name: 'required'
        }
    });

    $('#csv_form').validate({
        rules: {
            sr_number: {
                required: true,
                digits: true
            },
            csv_name: 'required',
            csv_file: 'required'
        }
    });

    $('#bus_stop_form').validate({
        rules: {
            sr_number: {
                required: true,
                digits: true
            },
            csv_name: 'required',
            bus_stop_ids: 'required'
        }
    });

    var bus_stop_detail_rules = {};

    $('input[name^=street_id]').each(function() {
        bus_stop_detail_rules[$(this).attr('name')] = {
            required: true,
            digits: true
        };
    });

    $('input[name^=short_name]').each(function() {
        bus_stop_detail_rules[$(this).attr('name')] = 'required';
    });

    $('input[name^=long_name]').each(function() {
        bus_stop_detail_rules[$(this).attr('name')] = 'required';
    });

    $('#bus_stop_detail_form').validate({
        rules: bus_stop_detail_rules
    });

    $('#bus_service_form').validate({
        rules: {
            sr_number: {
                required: true,
                digits: true
            },
            csv_name: 'required',
            bus_service_ids: 'required'
        }
    });

    $('#bus_route_form').validate({
        rules: {
            sr_number: {
                required: true,
                digits: true
            },
            csv_name: 'required',
            bus_service_ids: 'required'
        }
    });
    
    $('#sql_form').validate({
        rules: {
            sql_name: 'required'
        }
    });
});