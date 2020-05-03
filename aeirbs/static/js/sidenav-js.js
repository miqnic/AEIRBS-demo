$(document).ready(function () {
    $('#sidebarCollapse').on('click', function () {
        $('#sidebar').toggleClass('active');
        if ($('#sidebar').hasClass('active')) {
            $('#logo-AEIRBS').hide();
            $('#logo').show();

            $('#dashboard').hide();
            $('#dashboard-logo').show();

            $('#masterlist').hide();
            $('#masterlist-logo').show();

            $('#reports').hide();
            $('#reports-logo').show();

            $('#audit').hide();
            $('#audit-logo').show();

            $('#incident').hide();
            $('#incident-logo').show();

            $('#summary').hide();
            $('#summary-logo').show();
        }
        else {
            $('#logo-AEIRBS').show();
            $('#logo').hide();

            $('#dashboard').show();
            $('#dashboard-logo').hide();

            $('#masterlist').show();
            $('#masterlist-logo').hide();

            $('#reports').show();
            $('#reports-logo').hide();

            $('#audit').show();
            $('#audit-logo').hide();

            $('#incident').show();
            $('#incident-logo').hide();

            $('#summary').show();
            $('#summary-logo').hide();
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