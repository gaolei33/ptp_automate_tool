/**
 * Author: Gao Lei
 * Date: 5/4/13
 * Time: 11:13 AM
 */

function set_current_link() {
    var current_url = $(location).attr('pathname');
    var $current_link = $('#menu').find('a[href="' + current_url + '"]');
    // add 'current' style for itself
    $current_link.addClass('current');
    // add 'current' style for its parent if exists
    $current_link.parents('.submenu').prev('a').addClass('current');
}

$(function() {
    // menu hover animations
    $('#menu').children('.menu-item').hover(function() {
        var $menu_item_hover = $(this);
        $menu_item_hover.data('timer', setTimeout(function() {
            $menu_item_hover.children('.submenu').stop().slideDown(200);
        }, 250));
    }, function() {
        var $menu_item_hover = $(this);
        clearTimeout($menu_item_hover.data('timer'));
        $menu_item_hover.children('.submenu').stop().slideUp(100);
    });

    // set current link
    set_current_link();
});