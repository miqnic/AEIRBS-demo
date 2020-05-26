
$(document).ready(function () {
    
    $(".masterlist").toggleClass("active");
    
    $('.masterlistTable').DataTable({
        "paging":false,
        searching: false,    
        "order": [],
        'columnDefs': [{
            "targets": [0],
            "orderable": false
        }]
    });
    $("label").css("font-size", "12px")
    $(".dataTables_info").css("font-size", "14px")

    //checkbox on-load (unchecked by default)
    $(".deleteCheckboxHeader").prop("checked", false);
    $('.deleteCheckbox').each(function (i, obj) {
        $(this).prop("checked", false);
    });

    //checkbox header on change functions
    $(".deleteCheckboxHeader").on('change', function () {
        if ($(this).prop("checked") == true) {
            $("#deleteSelectedUser").show();
            $('.deleteCheckbox').each(function (i, obj) {
                $(this).prop("checked", true);
            });
        } else {
            $("#deleteSelectedUser").hide();
            $('.deleteCheckbox').each(function (i, obj) {
                $(this).prop("checked", false);
            });
        }
    });

    //checkbox on change functions
    $(".deleteCheckbox").on('change', function () {
        var checked = false;
        $('.deleteCheckbox').each(function (i, obj) {
            if ($(this).prop("checked") == true) {
                checked = true;
            }
        });

        if (checked) {
            $("#deleteSelectedUser").show();
        } else {
            $("#deleteSelectedUser").hide();
        }
    });

    $("#deleteSelectedUser").click(function () {
        var username_list = []
        $('.deleteCheckbox').each(function (i, obj) {
            if ($(this).prop("checked") == true) {
                var deleteID = $(this).data("delete");
                username_list.push(deleteID);
            }
        });
        $('#deleteList_input').val(username_list);
    });

    $(".table-masterlist").click(function() {
        if ($(".userDetails").is(':visible')){
            $(".userDetails").hide();

            var username = $(this).data("username");
            var id = "#userDetails" + username;
            $(".left-padding").width("65%");
            $(".user").css("padding", "0 25px 25px 25px");
            $(".userContainer").css("padding", "0 12.5px 25px 25px");
            $(id).show();
        }
        else{
            var username = $(this).data("username");
            var id = "#userDetails" + username;
            $(".left-padding").width("65%");
            $(".user").css("padding", "0 25px 25px 25px");
            $(".userContainer").css("padding", "0 12.5px 25px 25px");
            $(id).show();
        }
    });

    //Close Admin Details
    $(".closeAdmin").click(function() {
        var username = $(this).data("username");
        var id = "#userDetails" + username;

        $(".left-padding").width("100%");
        $(".userContainer").css("padding", "0 25px 25px 25px");
        $(id).hide();
    });

    $(".confirmDeleteButton").click(function () {
        var deleteID = "#delete" + $(this).data("delete");
        $(deleteID).submit();
      });
    
      $(".confirmEditButton").click(function () {
        var editID = "#edit" + $(this).data("edit");
        $(editID).submit();
      });
    
      $(".confirmAddButton").click(function () {
        var type = "#add" + $(this).data("add");
        $(type).submit();
      });
});