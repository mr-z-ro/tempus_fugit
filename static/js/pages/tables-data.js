(function () {
  $.turbo.execute(".tables-data-page", function() {
    $("#example1").DataTable();
    $('#example2').DataTable({
      destroy : true,
      paging: true,
      lengthChange: false,
      searching: false,
      ordering: true,
      info: true,
      autoWidth: false
    });
  })
})()
