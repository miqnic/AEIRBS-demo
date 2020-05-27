
$(document).ready(function () {
$('.incidentTable').DataTable({
  "paging": false,
  searching: false,
  "order": [2, "desc"],
  'columnDefs': [{
      "targets": [3],
      "orderable": false
  }]
});
});