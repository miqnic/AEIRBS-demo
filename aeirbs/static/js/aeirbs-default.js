$(document).ready(function () {
    $('.table').DataTable({
        "paging":false,
        searching: false
    });
    $("label").css("font-size", "14px")
    $(".dataTables_info").css("font-size", "14px")

    window.setTimeout(function () {
        $(".alert").fadeTo(500, 0).slideUp(500, function () {
            $(this).remove();
        });
    }, 4000);
});

