$(function() {
  var screenSizes =  {
    xs: 480,
    sm: 768,
    md: 992,
    lg: 1200
  }

  $(document).on("click", "[data-toggle='offcanvas']", function (e) {
    e.preventDefault()

    if ($(window).width() > (screenSizes.sm - 1)) {
      if ($("body").hasClass('sidebar-collapse')) {
        $("body")
          .removeClass('sidebar-collapse')
          .trigger('expanded.pushMenu')
      } else {
        $("body")
          .addClass('sidebar-collapse')
          .trigger('collapsed.pushMenu')
      }

    } else {
      if ($("body").hasClass('sidebar-open')) {
        $("body")
          .removeClass('sidebar-open')
          .removeClass('sidebar-collapse')
          .trigger('collapsed.pushMenu')
      } else {
        $("body")
          .addClass('sidebar-open')
          .trigger('expanded.pushMenu')
      }
    }

  })
})
