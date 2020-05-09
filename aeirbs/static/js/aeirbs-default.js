$(document).ready(function () {
    $('.dataTable').DataTable({
        "paging": false,
        searching: false,
        "order": [0, "desc"]
    });
    $("label").css("font-size", "12px")
    $(".dataTables_info").css("font-size", "14px")


    $('[data-toggle="popover"]').popover();

    window.setTimeout(function () {
        $(".alert").fadeTo(500, 0).slideUp(500, function () {
            $(this).remove();
        });
    }, 4000);
});

