$(document).on("click", ".sidebar li a", function (e) {
  var animationSpeed = 300

  var $this = $(this),
    $nextElement = $this.next(),
    menuClass = ".treeview-menu"

  if (
    ($nextElement.is(menuClass)) &&
    ($nextElement.is(":visible"))
  ) {
    $nextElement.slideUp(animationSpeed, function () {
      $nextElement.removeClass("menu-open")
    });
    $nextElement.parent("li").removeClass("active")
  }
  else if (
    ($nextElement.is(menuClass)) &&
    (!$nextElement.is(":visible"))
  ) {
    var $parent = $this.parents("ul").first();
    var $ul = $parent.find("ul:visible").slideUp(animationSpeed);
    $ul.removeClass("menu-open");
    var $parentLi = $this.parent("li");

    $nextElement.slideDown(animationSpeed, function () {
      $nextElement.addClass("menu-open");
      $parent.find("li.active").removeClass("active");
      $parentLi.addClass("active");
    });
  }
  if ($nextElement.is(menuClass)) {
    e.preventDefault();
  }

});

(function() {
  $.turbo.execute(".main-sidebar", function() {
    var animationSpeed = 300

    // Activate current link
    // In production version, you might want to
    // use a backend (server-side) implementation
    // to add 'active' class to the current link.
    var currentPath = window.location.pathname

    $(".main-sidebar .active").removeClass("active")

    if(currentPath == "/") {
      var $currentLink = $(".sidebar a[href='/index.html']")
    } else {
      var $currentLink = $(".sidebar a[href='" + currentPath + "']")
    }

    if($currentLink && $currentLink.length) {
      $currentLink.parent().addClass("active")
      $currentLink.parents("li.treeview").addClass("menu-open active")
      $currentLink.parents("ul").first().slideDown(animationSpeed)
    }
  })

})()
