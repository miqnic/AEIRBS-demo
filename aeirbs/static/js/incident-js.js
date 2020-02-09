$(document).ready(function(){
    //SIDENAV
    $('#logo-AEIRBS').show();
    $('#logo').hide();

    $('#dashboard').show();
    $('#dashboard-logo').hide();

    $('#masterlist').show();
    $('#masterlist-logo').hide();

    $('#reports').show();
    $('#reports-logo').hide();

    $('#audit').show();
    $('#audit-logo').hide();

    $('#incident').show();
    $('#incident-logo').hide();

    $('#summary').show();
    $('#summary-logo').hide();

    $('#sidebarCollapse').on('click', function () {
      $('#sidebar').toggleClass('active');
      if($('#sidebar').hasClass('active')){
        $('#logo-AEIRBS').hide();
        $('#logo').show();

        $('#dashboard').hide();
        $('#dashboard-logo').show();

        $('#masterlist').hide();
        $('#masterlist-logo').show();

        $('#reports').hide();
        $('#reports-logo').show();

        $('#audit').hide();
        $('#audit-logo').show();

        $('#incident').hide();
        $('#incident-logo').show();

        $('#summary').hide();
        $('#summary-logo').show();
      }
      else{
        $('#logo-AEIRBS').show();
        $('#logo').hide();

        $('#dashboard').show();
        $('#dashboard-logo').hide();

        $('#masterlist').show();
        $('#masterlist-logo').hide();

        $('#reports').show();
        $('#reports-logo').hide();

        $('#audit').show();
        $('#audit-logo').hide();

        $('#incident').show();
        $('#incident-logo').hide();

        $('#summary').show();
        $('#summary-logo').hide();
      }
    });
    //Add Image
    $(".imgAdd").click(function(){
      $(this).closest(".row").find('.imgAdd').before('<div class="col-sm-2 imgUp"><div class="imagePreview"></div><label class="btn btn-primary">Upload<input type="file" class="uploadFile img" value="Upload Photo" style="width:0px;height:0px;overflow:hidden;"></label><i class="fa fa-times del"></i></div>');
    });
    $(document).on("click", "i.del" , function() {
      $(this).parent().remove();
    });
    $(function() {
      $(document).on("change",".uploadFile", function()
      {
        var uploadFile = $(this);
        var files = !!this.files ? this.files : [];
        if (!files.length || !window.FileReader) return; // no file selected, or no FileReader support

        if (/^image/.test( files[0].type)){ // only image file
          var reader = new FileReader(); // instance of the FileReader
          reader.readAsDataURL(files[0]); // read the local file

          reader.onloadend = function(){ // set image data as background of div
            //alert(uploadFile.closest(".upimage").find('.imagePreview').length);
            uploadFile.closest(".imgUp").find('.imagePreview').css("background-image", "url("+this.result+")");
          }
        }

      });
    });
  });