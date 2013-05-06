/**
 * Author: Gao Lei
 * Date: 5/6/13
 * Time: 6:17 PM
 */


$(function() {
    $('form').validate({
        rules: {
            sr_number: {
                required: true,
                minlength: 2
            }
        }
    });
});