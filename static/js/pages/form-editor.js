(function () {
  $.turbo.execute(".forms-editor-page", function() {
    $(".textarea").wysihtml5()
    $("#summernote-editor").summernote({
      height: 300
    })

    $(window).off("pjax:unload").on("pjax:unload", function() {
      $("#summernote-editor").summernote('destroy')
    })


  })
})()
