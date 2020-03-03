$(document).ready(function() {
    $("#auditDetails").hide();

    //Clickble Rows
    $(".table-row").click(function() {
        $(".left-padding").width("65%");
        $("#auditTable").css("padding", "0 12.5px 25px 25px");
        $("#auditDetails").show();
    });

    //Close Audit Details
    $("#close-auditDetails").click(function() {
        $(".left-padding").width("100%");
        $("#audits").css("padding", "0 25px 25px 25px");
        $("#auditDetails").hide();
    });
});