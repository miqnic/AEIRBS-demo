
$(document).ready(function () {
$('.incidentTable').DataTable({
  "paging": true,
  "pagingType": "first_last_numbers",
  searching: false,
  "order": [2, "desc"],
  'columnDefs': [{
      "targets": [3],
      "orderable": false
  }],
  columnDefs: [       
    { type: 'date-euro', targets: 2 },
  ]
});
});