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


    $("#auditDetails").hide();

    //Clickble Rows
    $(".table-row").click(function() {
      $(".left-padding").width("65%");
      $("#audits").css("padding", "0 12.5px 25px 25px");
      $("#auditDetails").show();
    });

    //Close Audit Details
    $("#close-auditDetails").click(function() {
      $(".left-padding").width("100%");
      $("#audits").css("padding", "0 25px 25px 25px");
      $("#auditDetails").hide();
    });
  });