/**
 * User: Gao Lei
 * Date: 5/4/13
 * Time: 11:13 AM
 */

function set_current_link(current_url) {
    var $current_link = $('#menu').find('a[href="' + current_url + '"]');
    // add 'current' style for itself
    $current_link.addClass('current');
    // add 'current' style for its parent if exists
    $current_link.parents('.submenu').prev('a').addClass('current');
}

$(function() {
    // menu hover animations
    $('#menu').children('li').hover(function() {
        $(this).children('.submenu').slideDown(200);
    }, function() {
        $(this).children('.submenu').slideUp(100);
    });
    // set current link
    var current_url = $(location).attr('pathname');
    set_current_link(current_url);
});