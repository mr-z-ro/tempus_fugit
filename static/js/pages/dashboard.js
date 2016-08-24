(function() {
  $.turbo.execute(".dashboard-page", function() {
    'use strict';

    if ($("#salesChart").length) {

      var MONTHS = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"];

      var randomScalingFactor = function() {
        return Math.round(Math.random() * 100 * (Math.random() > 0.5 ? -1 : 1));
      };
      var randomColorFactor = function() {
        return Math.round(Math.random() * 200);
      };
      var randomColor = function(opacity) {
        return 'rgba(' + randomColorFactor() + ',' + randomColorFactor() + ',' + randomColorFactor() + ',' + (opacity || '0.7') + ')';
      };

      var salesChartconfig = {
        type: 'line',
        data: {
          labels: ["January", "February", "March", "April", "May", "June", "July"],
          datasets: [{
            label: "My First dataset",
            data: [randomScalingFactor(), randomScalingFactor(), randomScalingFactor(), randomScalingFactor(), randomScalingFactor(), randomScalingFactor(), randomScalingFactor()],
          }, {
            label: "My Second dataset",
            data: [randomScalingFactor(), randomScalingFactor(), randomScalingFactor(), randomScalingFactor(), randomScalingFactor(), randomScalingFactor(), randomScalingFactor()],
          }, {
            label: "My Third dataset",
            data: [randomScalingFactor(), randomScalingFactor(), randomScalingFactor(), randomScalingFactor(), randomScalingFactor(), randomScalingFactor(), randomScalingFactor()],
          }, {
            label: "My Third dataset",
            data: [randomScalingFactor(), randomScalingFactor(), randomScalingFactor(), randomScalingFactor(), randomScalingFactor(), randomScalingFactor(), randomScalingFactor()],
          }]
        },
        options: {
          responsive: true,
          title:{
            display: false,
          },
          tooltips: {
            mode: 'label',
          },
          hover: {
            mode: 'label'
          },
          legend: {
            display: false
          },
          scales: {
            xAxes: [{
              scaleLabel: {
                display: true,
                labelString: 'Month'
              }
            }],
            yAxes: [{
              stacked: true,
              scaleLabel: {
                display: true,
                labelString: 'Value'
              }
            }]
          }
        }
      };

      $.each(salesChartconfig.data.datasets, function(i, dataset) {
        var color = randomColor(1);
        dataset.borderColor = color;
        dataset.backgroundColor = color;
        dataset.pointBorderColor = color;
        dataset.pointBackgroundColor = color;
        dataset.pointBorderWidth = 1;
      });

      var ctx = $("#salesChart").get(0).getContext("2d");
      var salesChart = new Chart(ctx, salesChartconfig);
    }


    if ($("#pieChart").length) {
      //-------------
      //- PIE CHART -
      //-------------
      // Get context with jQuery - using jQuery's .get() method.
      var ctx = $("#pieChart").get(0).getContext("2d");
      var pieConfig =  {
        type: 'pie',
        data: {
          datasets: [{
            data: [300, 50, 100, 40, 10],
            backgroundColor: [
              "#F7464A",
              "#46BFBD",
              "#FDB45C",
              "#949FB1",
              "#4D5360",
            ],
          }],
          labels: [
            "Chrome",
            "IE",
            "Firefox",
            "Safari",
            "Opera"
          ]
        },
        options: {
          responsive: true,
          legend: {
            display: false
          }
        }
      };
      var pieChart = new Chart(ctx, pieConfig);
    }




    /* jVector Maps
    * ------------
    * Create a world map with markers
    */

    if ($("#world-map-markers").length) {
      $('#world-map-markers').vectorMap({
        map: 'world_mill_en',
        normalizeFunction: 'polynomial',
        hoverOpacity: 0.7,
        hoverColor: false,
        backgroundColor: 'transparent',
        regionStyle: {
          initial: {
            fill: 'rgba(210, 214, 222, 1)',
            "fill-opacity": 1,
            stroke: 'none',
            "stroke-width": 0,
            "stroke-opacity": 1
          },
          hover: {
            "fill-opacity": 0.7,
            cursor: 'pointer'
          },
          selected: {
            fill: 'yellow'
          },
          selectedHover: {}
        },
        markerStyle: {
          initial: {
            fill: '#00a65a',
            stroke: '#111'
          }
        },
        markers: [{
          latLng: [41.90, 12.45],
          name: 'Vatican City'
        }, {
          latLng: [43.73, 7.41],
          name: 'Monaco'
        }, {
          latLng: [-0.52, 166.93],
          name: 'Nauru'
        }, {
          latLng: [-8.51, 179.21],
          name: 'Tuvalu'
        }, {
          latLng: [43.93, 12.46],
          name: 'San Marino'
        }, {
          latLng: [47.14, 9.52],
          name: 'Liechtenstein'
        }, {
          latLng: [7.11, 171.06],
          name: 'Marshall Islands'
        }, {
          latLng: [17.3, -62.73],
          name: 'Saint Kitts and Nevis'
        }, {
          latLng: [3.2, 73.22],
          name: 'Maldives'
        }, {
          latLng: [35.88, 14.5],
          name: 'Malta'
        }, {
          latLng: [12.05, -61.75],
          name: 'Grenada'
        }, {
          latLng: [13.16, -61.23],
          name: 'Saint Vincent and the Grenadines'
        }, {
          latLng: [13.16, -59.55],
          name: 'Barbados'
        }, {
          latLng: [17.11, -61.85],
          name: 'Antigua and Barbuda'
        }, {
          latLng: [-4.61, 55.45],
          name: 'Seychelles'
        }, {
          latLng: [7.35, 134.46],
          name: 'Palau'
        }, {
          latLng: [42.5, 1.51],
          name: 'Andorra'
        }, {
          latLng: [14.01, -60.98],
          name: 'Saint Lucia'
        }, {
          latLng: [6.91, 158.18],
          name: 'Federated States of Micronesia'
        }, {
          latLng: [1.3, 103.8],
          name: 'Singapore'
        }, {
          latLng: [1.46, 173.03],
          name: 'Kiribati'
        }, {
          latLng: [-21.13, -175.2],
          name: 'Tonga'
        }, {
          latLng: [15.3, -61.38],
          name: 'Dominica'
        }, {
          latLng: [-20.2, 57.5],
          name: 'Mauritius'
        }, {
          latLng: [26.02, 50.55],
          name: 'Bahrain'
        }, {
          latLng: [0.33, 6.73],
          name: 'São Tomé and Príncipe'
        }]
      });
    }


    /* SPARKLINE CHARTS
    * ----------------
    * Create a inline charts with spark line
    */

    //-----------------
    //- SPARKLINE BAR -
    //-----------------
    $('.sparkbar').each(function() {
      var $this = $(this);
      $this.sparkline('html', {
        type: 'bar',
        height: $this.data('height') ? $this.data('height') : '30',
        barColor: $this.data('color')
      });
    });

    //-----------------
    //- SPARKLINE PIE -
    //-----------------
    $('.sparkpie').each(function() {
      var $this = $(this);
      $this.sparkline('html', {
        type: 'pie',
        height: $this.data('height') ? $this.data('height') : '90',
        sliceColors: $this.data('color')
      });
    });

    //------------------
    //- SPARKLINE LINE -
    //------------------
    $('.sparkline').each(function() {
      var $this = $(this);
      $this.sparkline('html', {
        type: 'line',
        height: $this.data('height') ? $this.data('height') : '90',
        width: '100%',
        lineColor: $this.data('linecolor'),
        fillColor: $this.data('fillcolor'),
        spotColor: $this.data('spotcolor')
      });
    });


    //------------------
    //-     MAP        -
    //------------------
    var southWest = new google.maps.LatLng(40.744656, -74.005966);
    var northEast = new google.maps.LatLng(34.052234, -118.243685);
    var lngSpan = northEast.lng() - southWest.lng();
    var latSpan = northEast.lat() - southWest.lat();

    var markers = [];

    var myLatlng = new google.maps.LatLng(38.392303, -86.931067);

    var map = new google.maps.Map(document.getElementById("map-canvas"), {
      zoom: 4,
      center: myLatlng,
      disableDefaultUI: true,
      scrollwheel: false,
      navigationControl: false,
      mapTypeControl: false,
      scaleControl: false,
      draggable: false,
      mapTypeId: google.maps.MapTypeId.ROADMAP,
      styles: [{
        "featureType": "administrative",
        "elementType": "labels.text.fill",
        "stylers": [{
          "color": "#444444"
        }]
      }, {
        "featureType": "landscape",
        "elementType": "all",
        "stylers": [{
          "color": "#f2f2f2"
        }]
      }, {
        "featureType": "poi",
        "elementType": "all",
        "stylers": [{
          "visibility": "off"
        }]
      }, {
        "featureType": "road",
        "elementType": "all",
        "stylers": [{
          "saturation": -100
        }, {
          "lightness": 45
        }]
      }, {
        "featureType": "road.highway",
        "elementType": "all",
        "stylers": [{
          "visibility": "simplified"
        }]
      }, {
        "featureType": "road.arterial",
        "elementType": "labels.icon",
        "stylers": [{
          "visibility": "off"
        }]
      }, {
        "featureType": "transit",
        "elementType": "all",
        "stylers": [{
          "visibility": "off"
        }]
      }, {
        "featureType": "water",
        "elementType": "all",
        "stylers": [{
          "color": "#46bcec"
        }, {
          "visibility": "on"
        }]
      }]
    });

    // Create some markers
    var markers = [];
    var addMarker = function() {
      var location = new google.maps.LatLng(
        southWest.lat() + latSpan * Math.random(),
        southWest.lng() + lngSpan * Math.random()
      );

      var marker = new google.maps.Marker({
        position: location,
        map: map,
        animation: google.maps.Animation.DROP
      });

      markers.push(marker);

      if (markers.length >= 5) {
        var randIndex = Math.floor(Math.random() * markers.length)
        markers[randIndex].setMap(null)
        markers.splice(randIndex, 1)
      }

      if(markers.length < 15) setTimeout(addMarker, 1000)
    }

    setTimeout(addMarker, 1000);

  })
})()
