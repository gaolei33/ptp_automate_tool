/**
 * Author: Gao Lei
 * Date: 4/29/13
 * Time: 8:42 PM
 */

$(function() {

    $('#street_search_switcher').click(function() {

        $('#street_search_container').slideToggle(function() {
            $('#keyword').focus();
        });

    });

    $('#street_search_btn').click(function() {
        var $keyword = $('#keyword');
        var keyword = $keyword.val();
        var keyword_type = $('#keyword_type').val();

        if (keyword == '') {
            alert('Please input keyword for street searching.');
            $keyword.focus();
            return;
        }

        var url = '/webapp/street/street_search/?keyword=' + encodeURI(keyword) + '&keyword_type=' + encodeURI(keyword_type);
        $.getJSON(url, function(data) {

            var $street_search_result_container = $('#street_search_result');
            $street_search_result_container.children().remove();

            $street_search_result_container.append($('<div><span>Result : ' + $(data).length + ' found.</span></div>'));

            var $street_container = $('<table cellpadding="5" cellspacing="0" class="street">');
            $(data).each(function(index, street) {

                var $street_id_container = $('<tr>').append($('<td>ID</td>')).append($('<td>').append(street[0]));
                var $street_short_name_container = $('<tr>').append($('<td>Short Name</td>')).append($('<td>').append(street[1]));
                var $street_long_name_container = $('<tr>').append($('<td>Long Name</td>')).append($('<td>').append(street[2]));

                $street_container.append($street_id_container).append($street_short_name_container).append($street_long_name_container).append($('<tr><td colspan="2">&nbsp;</td></tr>>'));

                $street_search_result_container.append($street_container)
            });

        })
    });

});