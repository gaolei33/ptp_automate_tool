/**
 * User: Gao Lei
 * Date: 5/4/13
 * Time: 11:13 AM
 */

$(function() {
    $menu = $('#menu');
    $menu.children('li').hover(function() {
        $(this).children('.submenu').slideDown(200);
    }, function() {
        $(this).children('.submenu').slideUp(100);
    });

    var current_url = $(location).attr('pathname');
    var $current_link = $menu.find('a[href="' + current_url + '"]');
    $current_link.addClass('current');
    $current_link.parents('.submenu').prev('a').addClass('current');
});