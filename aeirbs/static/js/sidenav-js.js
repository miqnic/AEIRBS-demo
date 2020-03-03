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

    $("#dashboard").click(function () {
        $("#dashboard").toggleClass('active');
        $("#masterlist").removeClass("active");
        $("#reports").removeClass("active");
        $("#audit").removeClass("active");
        $("#incident").removeClass("active");
        $("#summary").removeClass("active");
    });

    $("#masterlist").click(function () {
        $("#dashboard").removeClass("active");
        $("#masterlist").toggleClass('active');
        $("#reports").removeClass("active");
        $("#audit").removeClass("active");
        $("#incident").removeClass("active");
        $("#summary").removeClass("active");
    });

    $("#reports").click(function () {
        $("#dashboard").removeClass("active");
        $("#masterlist").removeClass("active");
        $("#reports").toggleClass("active");
        $("#audit").removeClass("active");
        $("#incident").removeClass("active");
        $("#summary").removeClass("active");
    });

    $("#audit").click(function () {
        $("#dashboard").removeClass("active");
        $("#masterlist").removeClass("active");
        $("#reports").removeClass("active");
        $("#audit").toggleClass("active");
        $("#incident").removeClass("active");
        $("#summary").removeClass("active");
    });

    $("#incident").click(function () {
        $("#dashboard").removeClass("active");
        $("#masterlist").removeClass("active");
        $("#reports").removeClass("active");
        $("#audit").removeClass("active");
        $("#incident").toggleClass("active");
        $("#summary").removeClass("active");
    });

    $("#summary").click(function () {
        $("#dashboard").removeClass("active");
        $("#masterlist").removeClass("active");
        $("#reports").removeClass("active");
        $("#audit").removeClass("active");
        $("#incident").removeClass("active");
        $("#summary").toggleClass("active");
    });

    $("#dashboard-logo").click(function () {
        $("#dashboard-logo").toggleClass('active');
        $("#masterlist-logo").removeClass("active");
        $("#reports-logo").removeClass("active");
        $("#audit-logo").removeClass("active");
        $("#incident-logo").removeClass("active");
        $("#summary-logo").removeClass("active");
    });

    $("#masterlist-logo").click(function () {
        $("#dashboard-logo").removeClass("active");
        $("#masterlist-logo").toggleClass('active');
        $("#reports-logo").removeClass("active");
        $("#audit-logo").removeClass("active");
        $("#incident-logo").removeClass("active");
        $("#summary-logo").removeClass("active");
    });

    $("#reports-logo").click(function () {
        $("#dashboard-logo").removeClass("active");
        $("#masterlist-logo").removeClass("active");
        $("#reports-logo").toggleClass("active");
        $("#audit-logo").removeClass("active");
        $("#incident-logo").removeClass("active");
        $("#summary-logo").removeClass("active");
    });

    $("#audit-logo").click(function () {
        $("#dashboard-logo").removeClass("active");
        $("#masterlist-logo").removeClass("active");
        $("#reports-logo").removeClass("active");
        $("#audit-logo").toggleClass("active");
        $("#incident-logo").removeClass("active");
        $("#summary-logo").removeClass("active");
    });

    $("#incident-logo").click(function () {
        $("#dashboard-logo").removeClass("active");
        $("#masterlist-logo").removeClass("active");
        $("#reports-logo").removeClass("active");
        $("#audit-logo").removeClass("active");
        $("#incident-logo").toggleClass("active");
        $("#summary-logo").removeClass("active");
    });

    $("#summary-logo").click(function () {
        $("#dashboard-logo").removeClass("active");
        $("#masterlist-logo").removeClass("active");
        $("#reports-logo").removeClass("active");
        $("#audit-logo").removeClass("active");
        $("#incident-logo").removeClass("active");
        $("#summary-logo").toggleClass("active");
    });
});