$(document).ready(function () {

  //Device
  $(".editDeviceButton").click(function () {
    $(".editDeviceForm").show();
    $(".deviceActions").hide();
    $(".deviceDetails").hide();
  });
  $(".cancelEditDeviceButton").click(function () {
    $(".deviceDetails").show();
    $(".deviceActions").show();
    $(".editDeviceForm").hide();
  });

  //Sensor
  $(".editSensorButton").click(function () {
    $(".editSensorForm").show();
    $(".sensorActions").hide();
    $(".sensorDetails").hide();
  });
  $(".cancelEditSensorButton").click(function () {
    $(".sensorDetails").show();
    $(".sensorActions").show();
    $(".editSensorForm").hide();
  });

  //Component
  $(".editComponentButton").click(function () {
    $(".editComponentForm").show();
    $(".componentActions").hide();
    $(".componentDetails").hide();
    $(".componentTabs").hide();
  });
  $(".cancelEditComponentButton").click(function () {
    $(".componentDetails").show();
    $(".componentActions").show();
    $(".componentTabs").show();
    $(".editComponentForm").hide();
  });
  $(".tabData").click(function () {
    $(".componentActions").hide()
  });
  $(".tabDetails").click(function () {
    $(".componentActions").show()
  });

  //Add Image
  $(".imgAdd").click(function () {
    $(this).closest(".row").find('.imgAdd').before('<div class="col-sm-2 imgUp"><div class="imagePreview"></div><label class="btn btn-primary">Upload<input type="file" class="uploadFile img" value="Upload Photo" style="width:0px;height:0px;overflow:hidden;"></label><i class="fa fa-times del"></i></div>');
  });
  $(document).on("click", "i.del", function () {
    $(this).parent().remove();
  });
  $(function () {
    $(document).on("change", ".uploadFile", function () {
      var uploadFile = $(this);
      var files = !!this.files ? this.files : [];
      if (!files.length || !window.FileReader) return; // no file selected, or no FileReader support

      if (/^image/.test(files[0].type)) { // only image file
        var reader = new FileReader(); // instance of the FileReader
        reader.readAsDataURL(files[0]); // read the local file

        reader.onloadend = function () { // set image data as background of div
          //alert(uploadFile.closest(".upimage").find('.imagePreview').length);
          uploadFile.closest(".imgUp").find('.imagePreview').css("background-image", "url(" + this.result + ")");
        }
      }

    });
  });

  //not yet finalized
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

  
  $(".connectivity-disconnected").hide();

  //Display Component Status
  $(".component").click(function () {
    var componentID = $(this).data("component");
    

    if ($(".status-switch" + componentID).is(":checked")) {
      $(".statusValue" + componentID).val(0);
      $(".status" + componentID).css("background-color", "rgb(30, 132, 73, 0.5)");
      $(".status-inactive" + componentID).hide();
      $(".status-needsMaintenance" + componentID).hide();
      $(".status-underMaintenance" + componentID).hide();
      $(".maintenance-status" + componentID).addClass("m-2");
      $(".needsMaintenance" + componentID).hide();
      $(".underMaintenance" + componentID).hide();
    } else {
      $(".statusValue" + componentID).val(3);
      $(".status" + componentID).css("background-color", "rgb(97, 106, 107,0.5)");
      $(".status-active" + componentID).hide();
      $(".status-inactive" + componentID).show();
      $(".status-needsMaintenance" + componentID).hide();
      $(".status-underMaintenance" + componentID).hide();

      $(".maintenance-status" + componentID).removeClass("m-2");
      $(".maintenance-status" + componentID).addClass("m-3");
      $(".needsMaintenance" + componentID).show();
      $(".underMaintenance" + componentID).show();
    }
    if ($(".maintenance-needsMaintenance" + componentID).is(":checked")) {
      $(".statusValue" + componentID).val(2);
      $(".status" + componentID).css("background-color", "rgb(146, 43, 33, 0.5)");
      $(".switch" + componentID).hide();
      $(".status-active" + componentID).hide();
      $(".status-inactive" + componentID).hide();
      $(".status-needsMaintenance" + componentID).show();
      $(".status-underMaintenance" + componentID).hide();
      $(".maintenance-underMaintenance" + componentID).prop("checked", false);
    }

    if ($(".maintenance-underMaintenance" + componentID).is(":checked")) {
      $(".statusValue" + componentID).val(1);
      $(".status" + componentID).css("background-color", "rgb(183, 149, 11, 0.5)");
      $(".switch" + componentID).hide();
      $(".status-active" + componentID).hide();
      $(".status-inactive" + componentID).hide();
      $(".status-needsMaintenance" + componentID).hide();
      $(".status-underMaintenance" + componentID).show();
      $(".maintenance-needsMaintenance" + componentID).prop("checked", false);
    }

    //Update Component Status
    $(".checkbox").on('change', function () {
      $(".saveStatusButton" + componentID).show();
      $(".statusLabel" + componentID).addClass("mb-5");
    });

    $(".status-switch" + componentID).click(function () {
      if ($(this).prop("checked") == true) {
        $(".statusValue" + componentID).val(0);
        $(".status" + componentID).css("background-color", "rgb(30, 132, 73, 0.5)");
        $(".status-active" + componentID).show();
        $(".status-inactive" + componentID).hide();
        $(".status-needsMaintenance" + componentID).hide();
        $(".status-underMaintenance" + componentID).hide();

        $(".maintenance-status" + componentID).removeClass("m-3");
        $(".maintenance-status" + componentID).addClass("m-2");
        $(".needsMaintenance" + componentID).hide();
        $(".underMaintenance" + componentID).hide();
      }
      else if ($(this).prop("checked") == false) {
        $(".statusValue" + componentID).val(3);
        $(".status" + componentID).css("background-color", "rgb(97, 106, 107,0.5)");
        $(".status-active" + componentID).hide();
        $(".status-inactive" + componentID).show();
        $(".status-needsMaintenance" + componentID).hide();
        $(".status-underMaintenance" + componentID).hide();

        $(".maintenance-status" + componentID).removeClass("m-2");
        $(".maintenance-status" + componentID).addClass("m-3");
        $(".needsMaintenance" + componentID).show();
        $(".underMaintenance" + componentID).show();
      }
    });

    $(".maintenance-needsMaintenance" + componentID).click(function () {
      if ($(this).prop("checked") == true) {
        $(".statusValue" + componentID).val(2);
        $(".status" + componentID).css("background-color", "rgb(146, 43, 33, 0.5)");
        $(".switch" + componentID).hide();
        $(".status-active" + componentID).hide();
        $(".status-inactive" + componentID).hide();
        $(".status-needsMaintenance" + componentID).show();
        $(".status-underMaintenance" + componentID).hide();
        $(".maintenance-underMaintenance" + componentID).prop("checked", false);
      }
      else if ($(this).prop("checked") == false) {
        $(".status" + componentID).css("background-color", "rgb(97, 106, 107,0.5)");
        $('.status-switch' + componentID).prop('checked', false);
        $(".switch" + componentID).show();
        $(".status-active" + componentID).hide();
        $(".status-inactive" + componentID).show();
        $(".status-needsMaintenance" + componentID).hide();
        $(".status-underMaintenance" + componentID).hide();

        $(".maintenance-status" + componentID).removeClass("m-2");
        $(".maintenance-status" + componentID).addClass("m-3");
        $(".needsMaintenance" + componentID).show();
        $(".underMaintenance" + componentID).show();
      }
    });

    $(".maintenance-underMaintenance" + componentID).click(function () {
      if ($(this).prop("checked") == true) {
        $(".statusValue" + componentID).val(1);
        $(".status" + componentID).css("background-color", "rgb(183, 149, 11, 0.5)");
        $(".switch" + componentID).hide();
        $(".status-active" + componentID).hide();
        $(".status-inactive" + componentID).hide();
        $(".status-needsMaintenance" + componentID).hide();
        $(".status-underMaintenance" + componentID).show();
        $(".maintenance-needsMaintenance" + componentID).prop("checked", false);
      }
      else if ($(this).prop("checked") == false) {
        $(".status" + componentID).css("background-color", "rgb(97, 106, 107,0.5)");
        $('.status-switch' + componentID).prop('checked', false);
        $(".switch" + componentID).show();
        $(".status-active" + componentID).hide();
        $(".status-inactive" + componentID).show();
        $(".status-needsMaintenance" + componentID).hide();
        $(".status-underMaintenance" + componentID).hide();

        $(".maintenance-status" + componentID).removeClass("m-2");
        $(".maintenance-status" + componentID).addClass("m-3");
        $(".needsMaintenance" + componentID).show();
        $(".underMaintenance" + componentID).show();
      }
    });
  });

  //Component Data
  $(".earthquakeComponent").click(function () {
    var componentID = $(this).data("component");

    var earthquakeData = document.getElementById(componentID).getContext('2d');
    var earthquakeDataChart = new Chart(earthquakeData, {
      type: 'line',
      data: {
        labels: ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12'],
        datasets: [{
          label: 'Earthquake',
          data: [1, 3, 5, 7, 9, 11],
          lineTension: 0,
          backgroundColor: 'rgb(229, 191, 154, 0.3)',
          borderColor: 'rgb(229, 191, 154)',
          borderWidth: 3,
          pointBorderColor: 'rgb(229, 191, 154)',
          pointBackgroundColor: 'rgb(229, 191, 154, 0.8)',
          pointRadius: 3,
          pointHoverBackgroundColor: 'rgb(254, 193, 7)',
          pointHoverBorderColor: 'rgb(254, 193, 7)',
          pointHoverRadius: 5,
        }]
      },
      options: {
        legend: {
          display: false
        },
        scales: {
          yAxes: [{
            scaleLabel: {
              display: true,
              labelString: 'Magnitude',
              fontFamily: 'Montserrat',
              fontStyle: 'bold',
            }
          }],
          xAxes: [{
            scaleLabel: {
              display: true,
              labelString: 'Time Interval (seconds)',
              fontFamily: 'Montserrat',
              fontStyle: 'bold',
            }
          }],
        }
      }
    });
  });

  $(".fireComponent").click(function () {
    var componentID = $(this).data("component");

    var fireData = document.getElementById(componentID).getContext('2d');
    var fireDataChart = new Chart(fireData, {
      type: 'line',
      data: {
        labels: ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12'],
        datasets: [{
          label: 'Fire',
          data: [4, 23, 10, 12, 10],
          lineTension: 0,
          backgroundColor: 'rgba(255, 126, 103, 0.3)',
          borderColor: 'rgba(255, 126, 103)',
          borderWidth: 3,
          pointBorderColor: 'rgba(255, 126, 103)',
          pointBackgroundColor: 'rgba(255, 126, 103, 0.8)',
          pointRadius: 3,
          pointHoverBackgroundColor: 'rgb(254, 193, 7)',
          pointHoverBorderColor: 'rgb(254, 193, 7)',
          pointHoverRadius: 5,
        }]
      },
      options: {
        legend: {
          display: false
        },
        scales: {
          yAxes: [{
            scaleLabel: {
              display: true,
              labelString: 'Temperature',
              fontFamily: 'Montserrat',
              fontStyle: 'bold',
            }
          }],
          xAxes: [{
            scaleLabel: {
              display: true,
              labelString: 'Time Interval (seconds)',
              fontFamily: 'Montserrat',
              fontStyle: 'bold',
            }
          }],
        }
      }
    });
  });

  $(".floodComponent").click(function () {
    var componentID = $(this).data("component");

    var floodData = document.getElementById(componentID).getContext('2d');
    var floodDataChart = new Chart(floodData, {
      type: 'line',
      data: {
        labels: ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12'],
        datasets: [{
          label: 'Flood',
          data: [12, 19, 3, 5, 2, 3],
          lineTension: 0,
          backgroundColor: 'rgba(162, 213, 242, 0.3)',
          borderColor: 'rgba(162, 213, 242)',
          borderWidth: 3,
          pointBorderColor: 'rgba(162, 213, 242)',
          pointBackgroundColor: 'rgba(162, 213, 242, 0.8)',
          pointRadius: 3,
          pointHoverBackgroundColor: 'rgb(254, 193, 7)',
          pointHoverBorderColor: 'rgb(254, 193, 7)',
          pointHoverRadius: 5,
        }]
      },
      options: {
        legend: {
          display: false
        },
        scales: {
          yAxes: [{
            scaleLabel: {
              display: true,
              labelString: 'Flood Height (inches)',
              fontFamily: 'Montserrat',
              fontStyle: 'bold',
            }
          }],
          xAxes: [{
            scaleLabel: {
              display: true,
              labelString: 'Time Interval (seconds)',
              fontFamily: 'Montserrat',
              fontStyle: 'bold',
            }
          }],
        }
      }
    });
  });
});