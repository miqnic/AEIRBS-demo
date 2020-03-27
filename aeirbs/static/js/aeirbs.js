$(document).ready(function() {
    $('.table').DataTable({
        "paging": false,
        searching: false
    });

    $(".dataTables_paginate").addClass("btn btn-sm float-right")
    $("label").css("font-size", "14px")
    $(".dataTables_info").css("font-size", "14px")

    window.setTimeout(function () {
        $(".alert").fadeTo(500, 0).slideUp(500, function () {
            $(this).remove();
        });
    }, 4000);
});