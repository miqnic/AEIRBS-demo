
$(document).ready(function () {
    $('#masterlistTable').DataTable({
        "paging":false,
        searching: false,
    });
    $("label").css("font-size", "12px")
    $(".dataTables_info").css("font-size", "14px")
    //Add Image
    $(".imgAdd").click(function() {
        $(this).closest(".row").find('.imgAdd').before('<div class="col-sm-2 imgUp"><div class="imagePreview"></div><label class="btn btn-primary">Upload<input type="file" class="uploadFile img" value="Upload Photo" style="width:0px;height:0px;overflow:hidden;"></label><i class="fa fa-times del"></i></div>');
    });
    $(document).on("click", "i.del", function() {
        $(this).parent().remove();
    });
    $(function() {
        $(document).on("change", ".uploadFile", function() {
            var uploadFile = $(this);
            var files = !!this.files ? this.files : [];
            if (!files.length || !window.FileReader) return; // no file selected, or no FileReader support

            if (/^image/.test(files[0].type)) { // only image file
                var reader = new FileReader(); // instance of the FileReader
                reader.readAsDataURL(files[0]); // read the local file

                reader.onloadend = function() { // set image data as background of div
                    //alert(uploadFile.closest(".upimage").find('.imagePreview').length);
                    uploadFile.closest(".imgUp").find('.imagePreview').css("background-image", "url(" + this.result + ")");
                }
            }
        });
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