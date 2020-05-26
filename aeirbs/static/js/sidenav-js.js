$(document).ready(function () {
    $('#sidebarCollapse').on('click', function () {
        $('#sidebar').toggleClass('active');
        if ($('#sidebar').hasClass('active')) {
            $('#logo-AEIRBS').hide();
            $('#logo').show();
        }
        else {
            $('#logo-AEIRBS').show();
            $('#logo').hide();
        }
    });
    
    $('.reports').click(function () {
        if ($("#pageSubmenu").is(":visible")) {
            $("#pageSubmenu").hide();
        } else {
            $("#pageSubmenu").show();
        }
    });
});