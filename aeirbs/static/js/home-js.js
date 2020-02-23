$(document).ready(function () {
  //MAIN CONTENTS
  $("#inputSpecifiedName").hide();
  $("#addComponentForm").hide();
  $("#addComponentLabel").hide();


  //Earthquake Functions
  $("#earthquakeCategory" ).click(function() {
    $("#fire-close").hide();
    $("#fire-open").show();
    $("#flood-close").hide();
    $("#flood-open").show();
    $("#others-close").hide();
    $("#others-open").show();
    if ($("#earthquake-close").is(":visible")){
      $("#earthquake-close").hide();
      $("#earthquake-open").show();
    }else{
      $("#earthquake-close").show();
      $("#earthquake-open").hide();
    }
  });

  //Fire Functions
  $("#fireCategory" ).click(function() {
    $("#earthquake-close").hide();
    $("#earthquake-open").show();
    $("#flood-close").hide();
    $("#flood-open").show();
    $("#others-close").hide();
    $("#others-open").show();
    if ($("#fire-close").is(":visible")){
      $("#fire-close").hide();
      $("#fire-open").show();
    }else{
      $("#fire-close").show();
      $("#fire-open").hide();
    }
  });

  //Flood Functions
  $("#floodCategory" ).click(function() {
    $("#earthquake-close").hide();
    $("#earthquake-open").show();
    $("#fire-close").hide();
    $("#fire-open").show();
    $("#others-close").hide();
    $("#others-open").show();
    if ($("#flood-close").is(':visible')){
      $("#flood-close").hide();
      $("#flood-open").show();
    }else{
      $("#flood-close").show();
      $("#flood-open").hide();
    }
  });


  //Others Functions
  $("#othersCategory" ).click(function() {
    $("#earthquake-close").hide();
    $("#earthquake-open").show();
    $("#fire-close").hide();
    $("#fire-open").show();
    $("#flood-close").hide();
    $("#flood-open").show();
    if ($("#others-close").is(":visible")){
      $("#others-close").hide();
      $("#others-open").show();
    }else{
      $("#others-close").show();
      $("#others-open").hide();
    }
  });

  //Add Components Functions
  $("#addComponentButton" ).click(function() {
    $("#addComponentForm").show();
    $("#addComponentLabel").show();
    $("#dashboardLabel").hide();
    $("#addComponentButton").hide();
    $("#componentAccordion").hide();
    $("#searchComponent").hide();
    $("#dashboardHeader").hide();
  });

  $("#cancelAddComponent" ).click(function() {
    $("#addComponentForm").hide();
    $("#addComponentLabel").hide();
    $("#dashboardLabel").show();
    $("#addComponentButton").show();
    $("#componentAccordion").show();
    $("#searchComponent").show();
    $("#sortComponent").show();
    $("#dashboardHeader").show();
  });

  $('#selectComponentName').change(function () {
    var selectedId = $('option:selected', this).attr('id');
    if (selectedId == "selectSpecifyNameButton") {
      $("#inputSpecifiedName").show();
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

  $("#deleteComponentButton").click(function() {
    $('#componentModal').modal('toggle')
    $('#confirmationModal').modal('toggle')
  });

  $("#saveComponentButton").click(function() {
    $('#componentModal').modal('toggle')
    $('#confirmationModal').modal('toggle')
  });

  $("#submitComponent").click(function() {
    $('#confirmationModal').modal('toggle')
  });

  $("#confirmCancelButton").click(function() {
    $('#confirmationModal').modal('toggle')
    $('#componentModal').modal('toggle')
  });

  $("#confirmCancelAddButton").click(function() {
    $('#confirmationModal').modal('toggle')

    $("#addComponentForm").hide();
    $("#addComponentLabel").hide();
    $("#dashboardLabel").show();
    $("#addComponentButton").show();
    $("#componentAccordion").show();
    $("#searchComponent").show();
    $("#sortComponent").show();
  });

  $("#status").css("background-color", "rgb(30, 132, 73, 0.5)");
  $("#status-inactive").hide();
  $("#status-needsMaintenance").hide();
  $("#status-underMaintenance").hide();
  $("#maintenance-status").addClass("m-2");
  $("#needsMaintenance").hide();
  $("#underMaintenance").hide();
  $("#connectivity-disconnected").hide();

  $("#status-switch"). click(function(){
    if($(this). prop("checked") == true){
      $("#status").css("background-color", "rgb(30, 132, 73, 0.5)");
      $("#status-active").show();
      $("#status-inactive").hide();
      $("#status-needsMaintenance").hide();
      $("#status-underMaintenance").hide();

      $("#maintenance-status").removeClass("m-3");
      $("#maintenance-status").addClass("m-2");
      $("#needsMaintenance").hide();
      $("#underMaintenance").hide();
    }
    else if($(this). prop("checked") == false){
      $("#status").css("background-color", "rgb(97, 106, 107,0.5)");
      $("#status-active").hide();
      $("#status-inactive").show();
      $("#status-needsMaintenance").hide();
      $("#status-underMaintenance").hide();

      $("#maintenance-status").removeClass("m-2");
      $("#maintenance-status").addClass("m-3");
      $("#needsMaintenance").show();
      $("#underMaintenance").show();
    }
  });

  $("#maintenance-needsMaintenance"). click(function(){
    if($(this). prop("checked") == true){
      $("#status").css("background-color", "rgb(146, 43, 33, 0.5)");
      $(".switch").hide();
      $("#status-active").hide();
      $("#status-inactive").hide();
      $("#status-needsMaintenance").show();
      $("#status-underMaintenance").hide();
      $("#maintenance-underMaintenance").prop("checked", false);
    }
    else if($(this). prop("checked") == false){
      $("#status").css("background-color", "rgb(97, 106, 107,0.5)");
      $('#status-switch').prop('checked', false);
      $(".switch").show();
      $("#status-active").hide();
      $("#status-inactive").show();
      $("#status-needsMaintenance").hide();
      $("#status-underMaintenance").hide();

      $("#maintenance-status").removeClass("m-2");
      $("#maintenance-status").addClass("m-3");
      $("#needsMaintenance").show();
      $("#underMaintenance").show();
    }
  });

  $("#maintenance-underMaintenance"). click(function(){
    if($(this). prop("checked") == true){
      $("#status").css("background-color", "rgb(183, 149, 11, 0.5)");
      $(".switch").hide();
      $("#status-active").hide();
      $("#status-inactive").hide();
      $("#status-needsMaintenance").hide();
      $("#status-underMaintenance").show();
      $("#maintenance-needsMaintenance").prop("checked", false);
    }
    else if($(this). prop("checked") == false){
      $("#status").css("background-color", "rgb(97, 106, 107,0.5)");
      $('#status-switch').prop('checked', false);
      $(".switch").show();
      $("#status-active").hide();
      $("#status-inactive").show();
      $("#status-needsMaintenance").hide();
      $("#status-underMaintenance").hide();

      $("#maintenance-status").removeClass("m-2");
      $("#maintenance-status").addClass("m-3");
      $("#needsMaintenance").show();
      $("#underMaintenance").show();
    }
  });

  $("#componentIDForm").hide();
  $("#componentNameForm").hide();
  $("#componentTypeForm").hide();
  $("#componentLocationForm").hide();
  $("#specifyNameForm").hide();
  $(".saveComponentButton").hide();
  $(".cancelEditComponentButton").hide();

  $("#confirmDeleteComponent").hide();
  $("#confirmSaveComponent").hide();
  $("#confirmAddComponent").hide();

  $("#deleteComponentText").hide();
  $("#saveComponentText").hide();
  $("#addComponentText").hide();

  $("#confirmDeleteButton").hide();
  $("#confirmSaveButton").hide();
  $("#confirmCancelAddButton").hide();

  if($("#confirmAddComponent").is(":visible")){
    $("#confirmDeleteComponent").hide();
    $("#confirmSaveComponent").hide();
  }

  if($("#addComponentText").is(":visible")){
    $("#deleteComponentText").hide();
    $("#saveComponentText").hide();
  }

  $("#editComponent").click(function() {
    $("#editComponent" ).hide();
    $("#componentID").hide();
    $("#componentIDForm").show();
    $("#componentName").hide();
    $("#componentNameForm").show();
    $("#deleteComponentButton").hide();
    $("#saveComponentButton").show();
    $("#cancelEditComponentButton").show();
  });

  $("#cancelEditComponentButton").click(function() {
    $("#editComponent" ).show();
    $("#componentID").show();
    $("#componentIDForm").hide();
    $("#componentName").show();
    $("#componentNameForm").hide();
    $("#deleteComponentButton").show();
    $("#saveComponentButton").hide();
    $("#cancelEditComponentButton").hide();
  });

  $("#saveComponentButton").click(function() {
    /*
    $("#editComponent" ).show();
    $("#componentID").show();
    $("#componentIDForm").hide();
    $("#componentName").show();
    $("#componentNameForm").hide();
    $("#componentType").show();
    $("#componentTypeForm").hide();
    $("#componentLocation").show();
    $("#componentLocationForm").hide();
    $("#saveComponentButton").hide();
    $("#deleteComponentButton").show();
    $("#specifyNameForm").hide();
    */

    $("#confirmSaveComponent").show();
    $("#saveComponentText").show();
    $("#confirmSaveButton").show();

    $("#confirmDeleteComponent").hide();
    $("#confirmAddComponent").hide();

    $("#deleteComponentText").hide();
    $("#addComponentText").hide();

    $("#confirmDeleteButton").hide();
    $("#confirmAddButton").hide();
  });

  $("#deleteComponentButton").click(function() {
    $("#confirmDeleteComponent").show();
    $("#deleteComponentText").show();
    $("#confirmDeleteButton").show();

    $("#confirmSaveComponent").hide();
    $("#confirmAddComponent").hide();

    $("#saveComponentText").hide();
    $("#addComponentText").hide();

    $("#confirmSaveButton").hide();
    $("#confirmAddButton").hide();
  });

  $("#submitComponent" ).click(function() {
    $("#confirmAddComponent").show();
    $("#addComponentText").show();
    $("#confirmAddButton").show();
    $("#confirmCancelAddButton").show();

    $("#confirmDeleteComponent").hide();
    $("#confirmSaveComponent").hide();

    $("#deleteComponentText").hide();
    $("saveComponentText").hide();

    $("#confirmDeleteButton").hide();
    $("#confirmSaveButton").hide();

    $("#confirmCancelButton").hide();

    /*  $("#addComponentForm").hide();
    $("#addComponentLabel").hide();
    $("#dashboardLabel").show();
    $("#addComponentButton").show();
    $("#componentAccordion").show();
    $("#searchComponent").show();
    $("#dashboardHeader").show();*/
  });

  $('#componentNameForm').change(function () {
    var selectedId = $('option:selected', this).attr('id');
    if (selectedId == "specifyNameFormButton") {
      $("#specifyNameForm").show();
    }
  });

});