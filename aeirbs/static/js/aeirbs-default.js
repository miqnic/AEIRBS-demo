$(document).ready(function () {
    $('.dataTable').DataTable({
        "paging": false,
        searching: false,
        "order": [0, "desc"]
    });
    $("label").css("font-size", "12px")
    $(".dataTables_info").css("font-size", "14px")



});

