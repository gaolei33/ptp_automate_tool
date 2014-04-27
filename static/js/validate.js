/**
 * Author: Gao Lei
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
    var $bus_stop_detail_form = $('#BUS_STOP_DETAIL_FORM');

    $bus_stop_detail_form.find('input[name^=street_id]').each(function() {
        bus_stop_detail_rules[$(this).attr('name')] = {
            required: true,
            digits: true
        };
    });

    $bus_stop_detail_form.find('input[name^=short_name]').each(function() {
        bus_stop_detail_rules[$(this).attr('name')] = 'required';
    });

    $bus_stop_detail_form.find('input[name^=long_name]').each(function() {
        bus_stop_detail_rules[$(this).attr('name')] = 'required';
    });

    $bus_stop_detail_form.find('input[name^=longitude]').each(function() {
        bus_stop_detail_rules[$(this).attr('name')] = {
            required: true,
            number: true
        };
    });

    $bus_stop_detail_form.find('input[name^=latitude]').each(function() {
        bus_stop_detail_rules[$(this).attr('name')] = {
            required: true,
            number: true
        };
    });

    var address_detail_rules = {};
    var $address_detail_form = $('#ADDRESS_DETAIL_FORM');

    $address_detail_form.find('input[name^=block]').each(function() {
        address_detail_rules[$(this).attr('name')] = 'required';
    });

    $address_detail_form.find('input[name^=street_name]').each(function() {
        address_detail_rules[$(this).attr('name')] = 'required';
    });

    $address_detail_form.find('input[name^=longitude]').each(function() {
        address_detail_rules[$(this).attr('name')] = {
            required: true,
            number: true
        };
    });

    $address_detail_form.find('input[name^=latitude]').each(function() {
        address_detail_rules[$(this).attr('name')] = {
            required: true,
            number: true
        };
    });

    var rules_set = [{
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
        form_id: 'BUS_ROUTE_ADD_OR_UPDATE_FORM',
        rules: {
            sr_number: {
                required: true,
                digits: true
            },
            csv_name_ncs: 'required',
            csv_name_lta: 'required',
            bus_service_ids: 'required'
        },
        need_confirm: false
    }, {
        form_id: 'ADDRESS_ADD_FORM',
        rules: {
            postal_codes: 'required'
        },
        need_confirm: false
    }, {
        form_id: 'ADDRESS_DETAIL_FORM',
        rules: address_detail_rules,
        need_confirm: false
    }, {
        form_id: 'SQL_DOWNLOAD_FORM',
        rules: {
            sql_name: 'required'
        },
        need_confirm: false
    }, {
        form_id: 'SQL_MERGED_DOWNLOAD_FORM',
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
    }, {
        form_id: 'PDF_RENAME_FORM',
        rules: {
            pdf_zip_file: 'required'
        },
        need_confirm: false
    }];

    $(rules_set).each(function() {
        validate(this.form_id, this.rules, this.need_confirm);
    });

});