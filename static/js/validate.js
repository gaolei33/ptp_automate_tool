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
                number: true
            },
            backup_name: 'required'
        }
    });

    $('#csv_form').validate({
        rules: {
            sr_number: {
                required: true,
                number: true
            },
            csv_name: 'required',
            csv_file: 'required'
        }
    });

    $('#bus_stop_form').validate({
        rules: {
            sr_number: {
                required: true,
                number: true
            },
            csv_name: 'required',
            bus_stop_ids: 'required'
        }
    });

    var bus_stop_detail_rules = {};

    $('input[name^=street_id]').each(function() {
        bus_stop_detail_rules[$(this).attr('name')] = {
            required: true,
            number: true
        };
    });

    $('input[name^=short_name]').each(function() {
        bus_stop_detail_rules[$(this).attr('name')] = 'required';
    });

    $('input[name^=long_name]').each(function() {
        bus_stop_detail_rules[$(this).attr('name')] = 'required';
    });

    $('input[name^=wab_accessible]').each(function() {
        bus_stop_detail_rules[$(this).attr('name')] = {
            required: true,
            number: true,
            rangelength: [1, 1],
            range: [0, 1]
        };
    });

    $('input[name^=non_bus_stop]').each(function() {
        bus_stop_detail_rules[$(this).attr('name')] = {
            required: true,
            number: true,
            rangelength: [1, 1],
            range: [0, 1]
        };
    });

    $('input[name^=interchange]').each(function() {
        bus_stop_detail_rules[$(this).attr('name')] = {
            required: true,
            number: true,
            rangelength: [1, 1],
            range: [0, 1]
        };
    });

    $('#bus_stop_detail_form').validate({
        rules: bus_stop_detail_rules
    });

    $('#bus_service_form').validate({
        rules: {
            sr_number: {
                required: true,
                number: true
            },
            csv_name: 'required',
            bus_service_ids: 'required'
        }
    });

    $('#bus_route_form').validate({
        rules: {
            sr_number: {
                required: true,
                number: true
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