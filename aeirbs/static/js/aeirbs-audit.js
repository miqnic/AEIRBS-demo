$(document).ready(function() {
    $(".table-auditlist").click(function() {
        if ($(".auditDetails").is(':visible')){
            $(".auditDetails").hide();

            var auditid = $(this).data("auditid");
            var id = "#auditDetails" + auditid;
            $(".left-padding").width("65%");
            $(".auditContainer").css("padding", "0 12.5px 25px 25px");
            $(id).show();
        }
        else{
            var auditid = $(this).data("auditid");
            var id = "#auditDetails" + auditid;
            $(".left-padding").width("65%");
            $(".auditContainer").css("padding", "0 12.5px 25px 25px");
            $(id).show();
        }
    });

    //Close Audit Details
    $("#close-auditDetails").click(function() {
        $(".left-padding").width("100%");
        $("#audits").css("padding", "0 25px 25px 25px");
        $("#auditDetails").hide();
    });
});