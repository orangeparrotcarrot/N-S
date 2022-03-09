// this script gets loaded once the page is ready
$(document).ready(function () {

    // some jQuery to handle clicking the menu links
    $('ul.sidenav li').click(function () {
        var index = $(this).attr('data-index');
        $('.content').addClass('hidden');
        $('#' + index).removeClass('hidden');
        $('ul.sidenav li a').removeClass('active').addClass('inactive');
        $('a', this).removeClass('inactive').addClass('active');
    });

    $("#login").click(function (e) {
        e.preventDefault();
        $.post("login", {"username":$('#username')[0].value}, function (data) {
            $("#private").html(data);
        });
    });

    $("#stats").click(function (e) {
        e.preventDefault();
        $.post("stats", function (data) {
            $("#private").html(data);
        });
    });

    $("#list").click(function (e) {
        e.preventDefault();
        $.post("list", function (data) {
            $("#private").html(data);
        });
    });
});