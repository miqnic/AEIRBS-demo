$(document).ready(function () {
    $('.auditTable').DataTable({
        "paging": true, 
         "pagingType": "first_last_numbers",
        searching: false,
        "order": [3, "desc"],
        'columnDefs': [{
            "targets": [0],
            "orderable": false
        }],
        columnDefs: [       
            { type: 'date-euro', targets: 3 },
          ]
    });


    //Close Audit Details
    $(".closeAudit").click(function () {
        var auditid = $(this).data("auditid");
        var id = "#auditDetails" + auditid;

        $(".left-padding").width("100%");
        $(".auditContainer").css("padding", "0 25px 25px 25px");
        $(id).hide();
    });

    $(".confirmClearLogs").click(function () {
        var auditType = "#clear" + $(this).data("log");
        $(auditType).submit();
    });
});