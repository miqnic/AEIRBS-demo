$(".addJobPositionButton").click(function () {
    $("#add_position").submit();
});
$(".editJobPositionButton").click(function () {
    var jobID = $(this).data("job")
    $(".editJobPosition" + jobID).show();
    $(".jobPosition" + jobID).hide();
});
$(".saveJobPositionButton").click(function () {
    var jobID = $(this).data("job")
    $(".editJobPosition" + jobID).hide();
    $(".jobPosition" + jobID).show();
});

//Earthquake Functions
$("#earthquakeCategory").click(function () {
    $("#fire-close").hide();
    $("#fire-open").show();
    $("#flood-close").hide();
    $("#flood-open").show();
    $("#others-close").hide();
    $("#others-open").show();
    if ($("#earthquake-close").is(":visible")) {
        $("#earthquake-close").hide();
        $("#earthquake-open").show();
    } else {
        $("#earthquake-close").show();
        $("#earthquake-open").hide();
    }
});

//Fire Functions
$("#fireCategory").click(function () {
    $("#earthquake-close").hide();
    $("#earthquake-open").show();
    $("#flood-close").hide();
    $("#flood-open").show();
    $("#others-close").hide();
    $("#others-open").show();
    if ($("#fire-close").is(":visible")) {
        $("#fire-close").hide();
        $("#fire-open").show();
    } else {
        $("#fire-close").show();
        $("#fire-open").hide();
    }
});

//Flood Functions
$("#floodCategory").click(function () {
    $("#earthquake-close").hide();
    $("#earthquake-open").show();
    $("#fire-close").hide();
    $("#fire-open").show();
    $("#others-close").hide();
    $("#others-open").show();
    if ($("#flood-close").is(':visible')) {
        $("#flood-close").hide();
        $("#flood-open").show();
    } else {
        $("#flood-close").show();
        $("#flood-open").hide();
    }
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