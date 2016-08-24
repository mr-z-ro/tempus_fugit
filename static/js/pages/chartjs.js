(function () {
  $.turbo.execute(".chartjs-page", function() {
    var randomScalingFactor = function() {
      return (Math.random() > 0.5 ? 1.0 : -1.0) * Math.round(Math.random() * 100);
    };
    var randomColorFactor = function() {
      return Math.round(Math.random() * 255);
    };
    var randomColor = function() {
      return 'rgba(' + randomColorFactor() + ',' + randomColorFactor() + ',' + randomColorFactor() + ',.7)';
    };


    // -----------------------
    // Multi line bar chart
    // ------------------------
    var barChartData = {
      labels: ["January", "February", "March", "April", "May", "June", "July"],
      datasets: [{
        label: 'New York',
        backgroundColor: "rgba(74, 144, 226,0.8)",
        yAxisID: "y-axis-1",
        data: [randomScalingFactor(), randomScalingFactor(), randomScalingFactor(), randomScalingFactor(), randomScalingFactor(), randomScalingFactor(), randomScalingFactor()]
      }, {
        label: 'California',
        backgroundColor: "rgba(126, 211, 33,0.5)",
        yAxisID: "y-axis-2",
        data: [randomScalingFactor(), randomScalingFactor(), randomScalingFactor(), randomScalingFactor(), randomScalingFactor(), randomScalingFactor(), randomScalingFactor()]
      }, {
        label: 'Miami',
        backgroundColor: [randomColor(), randomColor(), randomColor(), randomColor(), randomColor(), randomColor(), randomColor()],
        yAxisID: "y-axis-1",
        data: [randomScalingFactor(), randomScalingFactor(), randomScalingFactor(), randomScalingFactor(), randomScalingFactor(), randomScalingFactor(), randomScalingFactor()]
      }]

    };


    var ctx = $("#barChartMulti").get(0).getContext("2d");
    var barChartMulti = Chart.Bar(ctx, {
      data: barChartData,
      options: {
        responsive: true,
        hoverMode: 'label',
        hoverAnimationDuration: 400,
        stacked: false,
        title:{
          display:true,
          text:"Temperature Comparision for US Cities"
        },
        scales: {
          yAxes: [{
            type: "linear", // only linear but allow scale type registration. This allows extensions to exist solely for log scale for instance
            display: true,
            position: "left",
            id: "y-axis-1",
          }, {
            type: "linear", // only linear but allow scale type registration. This allows extensions to exist solely for log scale for instance
            display: true,
            position: "right",
            id: "y-axis-2",
            gridLines: {
              drawOnChartArea: false
            }
          }],
        }
      }
    });


    var refreshBarChart = $("#refreshBarChartMulti")
    refreshBarChart.click(function(e) {
      e.preventDefault()

      $.each(barChartData.datasets, function(i, dataset) {
        if (Chart.helpers.isArray(dataset.backgroundColor)) {
          dataset.backgroundColor= [randomColor(), randomColor(), randomColor(), randomColor(), randomColor(), randomColor(), randomColor()];
        } else {
          dataset.backgroundColor= randomColor();
        }

        dataset.data = [randomScalingFactor(), randomScalingFactor(), randomScalingFactor(), randomScalingFactor(), randomScalingFactor(), randomScalingFactor(), randomScalingFactor()];

      });
      barChartMulti.update();
    })



    // -----------------------
    // Polar area chart
    // -----------------------

    var polarAreaConfig = {
      data: {
        datasets: [{
          data: [
            randomScalingFactor(),
            randomScalingFactor(),
            randomScalingFactor(),
            randomScalingFactor(),
            randomScalingFactor(),
          ],
          backgroundColor: [
            "#F7464A",
            "#46BFBD",
            "#FDB45C",
            "#949FB1",
            "#4D5360",
          ],
          label: 'Programming' // for legend
        }],
        labels: [
          "Red",
          "Green",
          "Yellow",
          "Grey",
          "Dark Grey"
        ]
      },
      options: {
        responsive: true,
        legend: {
          display: false
        },
        title: {
          display: true,
          text: 'Chart.js Polar Area Chart'
        },
        scale: {
          ticks: {
            beginAtZero: false
          },
          reverse: false
        },
        animation: {
          animateRotate: false,
          animateScale: true
        }
      }
    };

    var ctx = $("#polar-area-chart").get(0).getContext("2d");
    var polarAreaChart = Chart.PolarArea(ctx, polarAreaConfig);



    // --------------------------
    // Multi Line Label
    // --------------------------
    var multiLineConfig = {
      type: 'line',
      data: {
        labels: [["June","2015"], "July", "August", "September", "October", "November", "December", ["January","2016"],"February", "March", "April", "May"],
        datasets: [{
          label: "HTML5",
          data: [randomScalingFactor(), randomScalingFactor(), randomScalingFactor(), randomScalingFactor(), randomScalingFactor(), randomScalingFactor(), randomScalingFactor(), randomScalingFactor(), randomScalingFactor(), randomScalingFactor(), randomScalingFactor(), randomScalingFactor()],
          fill: false,
          borderDash: [5, 5],
        }, {
          hidden: true,
          label: 'JavaScript',
          data: [randomScalingFactor(), randomScalingFactor(), randomScalingFactor(), randomScalingFactor(), randomScalingFactor(), randomScalingFactor(), randomScalingFactor(), randomScalingFactor(), randomScalingFactor(), randomScalingFactor(), randomScalingFactor(), randomScalingFactor()],
        }, {
          label: "CSS3",
          data: [randomScalingFactor(), randomScalingFactor(), randomScalingFactor(), randomScalingFactor(), randomScalingFactor(), randomScalingFactor(), randomScalingFactor(), randomScalingFactor(), randomScalingFactor(), randomScalingFactor(), randomScalingFactor(), randomScalingFactor()],
        },{
          label: "PHP",
          data: [randomScalingFactor(), randomScalingFactor(), randomScalingFactor(), randomScalingFactor(), randomScalingFactor(), randomScalingFactor(), randomScalingFactor(), randomScalingFactor(), randomScalingFactor(), randomScalingFactor(), randomScalingFactor(), randomScalingFactor()],
        }]
      },
      options: {
        responsive: true,
        title:{
          display:true,
          text:'Programming Language Usage Comparision'
        },
        hover: {
          mode: 'dataset'
        },
        scales: {
          xAxes: [{
            display: true,
            scaleLabel: {
              show: true,
              labelString: 'Month'
            }
          }],
          yAxes: [{
            display: true,
            scaleLabel: {
              show: true,
              labelString: 'Value'
            },
            ticks: {
              suggestedMin: -10,
              suggestedMax: 250,
            }
          }]
        }
      }
    };

    $.each(multiLineConfig.data.datasets, function(i, dataset) {
      dataset.borderColor = randomColor(0.8);
      dataset.backgroundColor = randomColor(0.6);
      dataset.pointBorderColor = randomColor(0.7);
      dataset.pointBackgroundColor = randomColor(0.9);
      dataset.pointBorderWidth = 1;
    });

    var multiLineCtx = $("#multiLine").get(0).getContext("2d");
    var multiLine = new Chart(multiLineCtx, multiLineConfig);



    // ---------------------
    // Radar graph
    // ---------------------

    var radarConfig = {
      type: 'radar',
      data: {
        labels: ["Eating", "Drinking", "Sleeping", "Designing", "Coding", "Cycling", "Running"],
        datasets: [{
          label: "Iron Man",
          borderColor: 'rgb(255, 0, 0)',
          backgroundColor: "rgba(255,255,0,0.4)",
          pointBackgroundColor: "rgba(120,90,12,0.7)",
          data: [NaN, randomScalingFactor(), randomScalingFactor(), randomScalingFactor(), randomScalingFactor(), randomScalingFactor(), randomScalingFactor()]
        }, {
          label: "Captain America",
          borderColor: 'rgb(255, 0, 255)',
          backgroundColor: "rgba(0, 255, 0, 0.5)",
          pointBackgroundColor: "rgba(151,187,205,1)",
          hoverPointBackgroundColor: "#fff",
          pointHighlightStroke: "rgba(151,187,205,1)",
          data: [randomScalingFactor(), randomScalingFactor(), NaN, randomScalingFactor(), randomScalingFactor(), randomScalingFactor(), randomScalingFactor()]
        },{
          label: "Hawkeye",
          borderColor: 'rgb(0, 255, 255, 0.6)',
          backgroundColor: "rgba(0, 0, 255, 0.4)",
          pointBackgroundColor: "rgba(151,187,205,1)",
          hoverPointBackgroundColor: "#fff",
          pointHighlightStroke: "rgba(151,187,205,1)",
          data: [randomScalingFactor(), randomScalingFactor(), randomScalingFactor(), randomScalingFactor(), randomScalingFactor(), randomScalingFactor(), NaN]
        }]
      },
      options: {
        title:{
          display:true,
          text:"Daily Activities Time Chart"
        },
        legend: {
          position: "bottom"
        },
        elements: {
          line: {
            tension: 0.0,
          }
        },
        scale: {
          beginAtZero: true,
          reverse: false
        }
      }
    };

    var radarChart = new Chart($("#radarChart"), radarConfig);

    var refreshRadar = $("#refreshRadar");
    refreshRadar.click(function(e) {
      e.preventDefault()
      $.each(radarConfig.data.datasets, function(i, dataset) {
        dataset.data = dataset.data.map(function() {
          return randomScalingFactor();
        });
      });

      radarChart.update();
    })




    // --------------------
    // Bubble Chart
    // ---------------------
    var bubbleChartData = {
      animation: {
        duration: 10000
      },
      datasets: [{
        label: "China",
        backgroundColor: randomColor(),
        data: [{
          x: randomScalingFactor(),
          y: randomScalingFactor(),
          r: Math.abs(randomScalingFactor()) / 5,
        }, {
          x: randomScalingFactor(),
          y: randomScalingFactor(),
          r: Math.abs(randomScalingFactor()) / 5,
        }, {
          x: randomScalingFactor(),
          y: randomScalingFactor(),
          r: Math.abs(randomScalingFactor()) / 5,
        }, {
          x: randomScalingFactor(),
          y: randomScalingFactor(),
          r: Math.abs(randomScalingFactor()) / 5,
        }, {
          x: randomScalingFactor(),
          y: randomScalingFactor(),
          r: Math.abs(randomScalingFactor()) / 5,
        }, {
          x: randomScalingFactor(),
          y: randomScalingFactor(),
          r: Math.abs(randomScalingFactor()) / 5,
        }, {
          x: randomScalingFactor(),
          y: randomScalingFactor(),
          r: Math.abs(randomScalingFactor()) / 5,
        }]
      }, {
        label: "United States",
        backgroundColor: randomColor(),
        data: [{
          x: randomScalingFactor(),
          y: randomScalingFactor(),
          r: Math.abs(randomScalingFactor()) / 5,
        }, {
          x: randomScalingFactor(),
          y: randomScalingFactor(),
          r: Math.abs(randomScalingFactor()) / 5,
        }, {
          x: randomScalingFactor(),
          y: randomScalingFactor(),
          r: Math.abs(randomScalingFactor()) / 5,
        }, {
          x: randomScalingFactor(),
          y: randomScalingFactor(),
          r: Math.abs(randomScalingFactor()) / 5,
        }, {
          x: randomScalingFactor(),
          y: randomScalingFactor(),
          r: Math.abs(randomScalingFactor()) / 5,
        }, {
          x: randomScalingFactor(),
          y: randomScalingFactor(),
          r: Math.abs(randomScalingFactor()) / 5,
        }, {
          x: randomScalingFactor(),
          y: randomScalingFactor(),
          r: Math.abs(randomScalingFactor()) / 5,
        }]
      }, {
        label: "India",
        backgroundColor: randomColor(),
        data: [{
          x: randomScalingFactor(),
          y: randomScalingFactor(),
          r: Math.abs(randomScalingFactor()) / 5,
        }, {
          x: randomScalingFactor(),
          y: randomScalingFactor(),
          r: Math.abs(randomScalingFactor()) / 5,
        }, {
          x: randomScalingFactor(),
          y: randomScalingFactor(),
          r: Math.abs(randomScalingFactor()) / 5,
        }, {
          x: randomScalingFactor(),
          y: randomScalingFactor(),
          r: Math.abs(randomScalingFactor()) / 5,
        }, {
          x: randomScalingFactor(),
          y: randomScalingFactor(),
          r: Math.abs(randomScalingFactor()) / 5,
        }, {
          x: randomScalingFactor(),
          y: randomScalingFactor(),
          r: Math.abs(randomScalingFactor()) / 5,
        }, {
          x: randomScalingFactor(),
          y: randomScalingFactor(),
          r: Math.abs(randomScalingFactor()) / 5,
        }]
      }]
    };

    var ctx = $("#bubbleChart").get(0).getContext("2d");
    window.myChart = new Chart(ctx, {
      type: 'bubble',
      data: bubbleChartData,
      options: {
        responsive: true,
        title:{
          display:true,
          text:'Population Comparision'
        },
      }
    });

  })
})()
