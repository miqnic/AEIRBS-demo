$(document).ready(function() {
    $('.table').DataTable({
        "pagingType": "first_last_numbers",
        searching: false,
    });

    $(".dataTables_paginate").addClass("btn btn-sm float-right")
    $("label").css("font-size", "14px")
    $(".dataTables_info").css("font-size", "14px")
});