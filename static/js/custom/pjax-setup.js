(function ($) {
  $.turbo = {
    hasRun: false,
    execute: function(selector, callback) {
      $(document).ready(function() {
        if(!$.turbo.hasRun) {
          $(document).trigger("pjax:render")
          $.turbo.hasRun = true
        }
      })

      $(document).on("pjax:render", function() {
        if($(selector).length) callback()
      })
    }
  }
}(jQuery))

$(function() {
  $.pjax({
    link: '[data-pjax]',
    wait: 400,
    area: [
      '.content-wrapper-inner',
    ],
    load: {
      head: 'meta, title',
      css: true,
      script: true
    },
    cache: {
      click: true, submit: true, popstate: true,
      get: true, post: false
    },
    scrollTop: false
  })

  $(document).on("pjax:fetch", function() {
    $.turbo.hasRun = false
  })

  // Transition
  var $transitionContainer = $(".content-wrapper-transition")
  var $pageLoader = $(".page-loader")

  $(document).bind('pjax:fetch', function() {
    $("body").animate({
      scrollTop: 0
    }, {
      queue: false,
      duration: 300
    })

    $pageLoader.fadeIn()

    $transitionContainer.animate({
      top: 100,
      opacity: 0
    }, {
      queue: false,
      duration: 400
    })

    // $("body > *").not(".wrapper").remove()
  })

  $(document).bind('pjax:render', function() {
    $pageLoader.fadeOut(function() {
      $transitionContainer.animate({
        top: 0,
        opacity: 1
      }, {
        queue: false,
        duration: 400
      }, function() {
        $(document).trigger("pjax:transitionComplete")
      })
    })
  })

})
