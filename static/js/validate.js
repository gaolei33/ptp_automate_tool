/**
 * User: Gao Lei
 * Date: 5/7/13
 * Time: 1:38 AM
 */


function validate(form_id, rules, need_confirm) {
    $('#' + form_id).validate({
        rules: rules,
        submitHandler: function(form) {
            if (need_confirm && !(confirm('Are you sure to proceed?'))) {
                return;
            }
            form.submit();
        }
    });
}


$(function() {

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

    $('input[name^=longitude]').each(function() {
        bus_stop_detail_rules[$(this).attr('name')] = {
            required: true,
            number: true
        };
    });

    $('input[name^=latitude]').each(function() {
        bus_stop_detail_rules[$(this).attr('name')] = {
            required: true,
            number: true
        };
    });

    rules_set = [{
        form_id: 'DB_BACKUP_FORM',
        rules: {
            sr_number: {
                required: true,
                digits: true
            }
        },
        need_confirm: false
    }, {
        form_id: 'DB_RESTORE_FORM',
        rules: {
            backup_name: 'required'
        },
        need_confirm: true
    }, {
        form_id: 'DB_BACKUP_DELETE_FORM',
        rules: {
            backup_name: 'required'
        },
        need_confirm: true
    }, {
        form_id: 'CSV_UPLOAD_FORM',
        rules: {
            sr_number: {
                required: true,
                digits: true
            },
            csv_file: 'required'
        },
        need_confirm: false
    }, {
        form_id: 'CSV_DELETE_FORM',
        rules: {
            csv_name: 'required'
        },
        need_confirm: true
    }, {
        form_id: 'BUS_STOP_ADD_FORM',
        rules: {
            sr_number: {
                required: true,
                digits: true
            },
            csv_name: 'required',
            bus_stop_ids: 'required'
        },
        need_confirm: false
    }, {
        form_id: 'BUS_STOP_UPDATE_FORM',
        rules: {
            sr_number: {
                required: true,
                digits: true
            },
            bus_stop_ids: 'required'
        },
        need_confirm: false
    }, {
        form_id: 'BUS_STOP_DETAIL_FORM',
        rules: bus_stop_detail_rules,
        need_confirm: false
    }, {
        form_id: 'BUS_SERVICE_ADD_OR_UPDATE_FORM',
        rules: {
            sr_number: {
                required: true,
                digits: true
            },
            csv_name: 'required',
            bus_service_ids: 'required'
        },
        need_confirm: false
    }, {
        form_id: 'BUS_SERVICE_ENABLE_OR_DISABLE_FORM',
        rules: {
            sr_number: {
                required: true,
                digits: true
            },
            bus_service_ids: 'required'
        },
        need_confirm: false
    }, {
        form_id: 'BUS_ROUTE_NCS_FORM',
        rules: {
            sr_number: {
                required: true,
                digits: true
            },
            csv_name: 'required',
            bus_service_ids: 'required'
        },
        need_confirm: false
    }, {
        form_id: 'BUS_ROUTE_LTA_FORM',
        rules: {
            sr_number: {
                required: true,
                digits: true
            },
            csv_name: 'required',
            bus_service_ids: 'required'
        },
        need_confirm: false
    }, {
        form_id: 'SQL_DOWNLOAD_FORM',
        rules: {
            sql_name: 'required'
        },
        need_confirm: false
    }, {
        form_id: 'SQL_DELETE_FORM',
        rules: {
            sql_name: 'required'
        },
        need_confirm: true
    }];

    $(rules_set).each(function() {
        validate(this.form_id, this.rules, this.need_confirm);
    });

});