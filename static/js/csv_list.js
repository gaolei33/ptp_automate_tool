/**
 * Author: Gao Lei
 * Date: 4/29/13
 * Time: 8:49 PM
 */

function get_csv_list(csv_type) {

    var url = '/webapp/get_csv_list/?csv_type=' + csv_type;

    $.getJSON(url, function(data) {

        var $csv_name = $('#csv_name');

        $csv_name.children().remove();

        $(data).each(function(index, csv_name) {
            var $option = $('<option>', {
                'value': csv_name,
                'text': csv_name
            });
            $csv_name.append($option);
        });

    });

}

$(function() {

    var $csv_type = $('#csv_type');

    $csv_type.change(function() {
        get_csv_list($(this).val());
    });

    if ($csv_type.children().length <= 1 ) {
        $csv_type.hide();
    }

    get_csv_list($csv_type.val());

});