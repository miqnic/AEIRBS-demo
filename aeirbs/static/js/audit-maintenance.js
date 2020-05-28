$(document).ready(function () {
    $(".table-auditlist").click(function () {
        if ($(".auditDetails").is(':visible')) {
            $(".auditDetails").hide();

            var auditid = $(this).data("auditid");
            var id = "#auditDetails" + auditid;
            $(".left-padding").width("65%");
            $(".auditContainer").css("padding", "0 12.5px 25px 25px");
            $(id).show();
        }
        else {
            var auditid = $(this).data("auditid");
            var id = "#auditDetails" + auditid;
            $(".left-padding").width("65%");
            $(".auditContainer").css("padding", "0 12.5px 25px 25px");
            $(id).show();
        }
    });
});