$(function() {
  var animationSpeed = 300

  $(document)
  .on("click", "[data-widget='collapse']", function(e) {
    e.preventDefault()
    var $this = $(this)
    var $box = $this.parents(".box").first()
    var $boxContent = $box.find("> .box-body, > .box-footer")

    if (!$box.hasClass("collapsed-box")) {
      $this.children().first()
        .removeClass("fa-minus")
        .addClass("fa-plus")

      $boxContent.slideUp(animationSpeed, function () {
        $box.addClass("collapsed-box")
      })

    } else {
      $this.children().first()
        .removeClass("fa-plus")
        .addClass("fa-minus")

      $boxContent.slideDown(animationSpeed, function () {
        $box.removeClass("collapsed-box")
      })

    }
  })
  .on("click", "[data-widget='remove']", function(e) {
    e.preventDefault()
    var $box = $(this).parents(".box").first()
    $box.slideUp(animationSpeed)
  })
})
