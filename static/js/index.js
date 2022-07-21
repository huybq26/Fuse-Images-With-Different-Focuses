$(document).ready(function () {
  console.log('loaded index.js');
  let uploaded = false;
  let length = 0;
  let dcl = 0;
  let df = 0;
  let doh = 0;
  let x = [];
  let y_cl = [];
  let y_f = [];
  let y_oh = [];
  let err_cl = [];
  let err_f = [];
  let err_oh = [];
  let num_plot = 0;
  let num_run = 0;

  // $(".button-upload").click(function () {
  //     let fd = new FormData();
  //     $excel = $('.upload #upload-file')[0].files[0];
  //     fd.append('excel', $excel);

  //     $.ajax({
  //         url: 'https://aptimer.wovodat.org/api/excel',
  //         type: 'post',
  //         data: fd,
  //         cache: false,
  //         contentType: false,
  //         processData: false,
  //         success: function (data) {
  //             console.log("success");
  //             console.log(data);

  //             x = data['x'];
  //             y_cl = data['y_cl'];
  //             y_f = data['y_f'];
  //             y_oh = data['y_oh'];
  //             err_cl = data['err_cl'];
  //             err_f = data['err_f'];
  //             err_oh = data['err_oh'];
  //             length = data['length'];

  //             var lineCl = {
  //                 x: x,
  //                 y: y_cl,
  //                 error_y: { array: err_cl, visible: true, color: 'black' },
  //                 name: 'Natural data',
  //                 mode: 'lines+markers',
  //                 line: { color: 'black', dash: 'dash', width: 2 },
  //                 type: 'scatter',
  //             };
  //             var lineF = {
  //                 x: x,
  //                 y: y_f,
  //                 xaxis: 'x2',
  //                 yaxis: 'y2',
  //                 error_y: { array: err_f, visible: true, color: 'black' },
  //                 mode: 'lines+markers',
  //                 line: { color: 'black', dash: 'dash', width: 2 },
  //                 type: 'scatter',
  //                 showlegend: false,
  //             };
  //             var lineOH = {
  //                 x: x,
  //                 y: y_oh,
  //                 xaxis: 'x3',
  //                 yaxis: 'y3',
  //                 error_y: { array: err_oh, visible: true, color: 'black' },
  //                 mode: 'lines+markers',
  //                 line: { color: 'black', dash: 'dash', width: 2 },
  //                 type: 'scatter',
  //                 showlegend: false,
  //             };
  //             var layout = {
  //                 grid: { rows: 1, columns: 3, pattern: 'independent' },
  //                 plot_bgcolor: "#ccedff",
  //                 xaxis: { dtick: 2, title: { text: "Distance (µm)" }, },
  //                 xaxis2: { dtick: 2, title: { text: "Distance (µm)" } },
  //                 xaxis3: { dtick: 2, title: { text: "Distance (µm)" } },
  //                 yaxis: { dtick: 0.01, title: { text: "X<sub>Cl</sub>" } },
  //                 yaxis2: { dtick: 0.05, title: { text: "X<sub>F</sub>" } },
  //                 yaxis3: { dtick: 0.05, title: { text: "X<sub>OH</sub>" } },
  //                 legend: { orientation: 'h', y: -0.25 },
  //             };

  //             Plotly.newPlot('plot', [lineCl, lineF, lineOH], layout);
  //             uploaded = true;
  //         },
  //         error: function (data) {
  //             console.log("error");
  //             alert("Incorrect format file");
  //         }
  //     });
  // });
  // $('#showBtn').on('click', function (data) {
  //   // const df = new DataFrame(data, columns);
  //   //           console.log("success");
  //   //           console.log(data);
  //   DataFrame.fromCSV('./cleaned_particles.csv').then((df) => df);
  //   console.log(df);

  //   //     x = data['x'];
  //   //     y_cl = data['y_cl'];
  //   //     y_f = data['y_f'];
  //   //     y_oh = data['y_oh'];
  //   //     err_cl = data['err_cl'];
  //   //     err_f = data['err_f'];
  //   //     err_oh = data['err_oh'];
  //   //     length = data['length'];

  //   //     var lineCl = {
  //   //         x: x,
  //   //         y: y_cl,
  //   //         error_y: { array: err_cl, visible: true, color: 'black' },
  //   //         name: 'Natural data',
  //   //         mode: 'lines+markers',
  //   //         line: { color: 'black', dash: 'dash', width: 2 },
  //   //         type: 'scatter',
  //   //     };
  //   //     var lineF = {
  //   //         x: x,
  //   //         y: y_f,
  //   //         xaxis: 'x2',
  //   //         yaxis: 'y2',
  //   //         error_y: { array: err_f, visible: true, color: 'black' },
  //   //         mode: 'lines+markers',
  //   //         line: { color: 'black', dash: 'dash', width: 2 },
  //   //         type: 'scatter',
  //   //         showlegend: false,
  //   //     };
  //   //     var lineOH = {
  //   //         x: x,
  //   //         y: y_oh,
  //   //         xaxis: 'x3',
  //   //         yaxis: 'y3',
  //   //         error_y: { array: err_oh, visible: true, color: 'black' },
  //   //         mode: 'lines+markers',
  //   //         line: { color: 'black', dash: 'dash', width: 2 },
  //   //         type: 'scatter',
  //   //         showlegend: false,
  //   //     };
  //   //     var layout = {
  //   //         grid: { rows: 1, columns: 3, pattern: 'independent' },
  //   //         plot_bgcolor: "#ccedff",
  //   //         xaxis: { dtick: 2, title: { text: "Distance (µm)" }, },
  //   //         xaxis2: { dtick: 2, title: { text: "Distance (µm)" } },
  //   //         xaxis3: { dtick: 2, title: { text: "Distance (µm)" } },
  //   //         yaxis: { dtick: 0.01, title: { text: "X<sub>Cl</sub>" } },
  //   //         yaxis2: { dtick: 0.05, title: { text: "X<sub>F</sub>" } },
  //   //         yaxis3: { dtick: 0.05, title: { text: "X<sub>OH</sub>" } },
  //   //         legend: { orientation: 'h', y: -0.25 },
  //   //     };

  //   //     Plotly.newPlot('plot', [lineCl, lineF, lineOH], layout);
  //   //     uploaded = true;
  // });

  $('.button-cal').click(function () {
    if (uploaded) {
      $('.calculation-result').empty();
      $temp = $('.diffusivity-cal #temp').val();
      $tilt = $('.diffusivity-cal #tilt').val();

      let url = 'https://aptimer.wovodat.org/api/diff';
      $.get(url, { temp: $temp, tilt: $tilt }, function (data, status) {
        console.log(status);
        if (status == 'success') {
          let diff = data['diffusivity'];
          dcl = diff['D(CL)'];
          df = diff['D(F)'];
          doh = diff['D(OH)'];

          $new_div =
            "<table class='table table-sm col-lg-5 col-md-8'>" +
            '<tr><th>D<sub>Cl</sub>:</th><td>' +
            dcl +
            '</td><td>m<sup>2</sup>/s</td></tr>' +
            '<tr><th>D<sub>F</sub>:</th><td>' +
            df +
            '</td><td>m<sup>2</sup>/s</td></tr>' +
            '<tr><th>D<sub>OH</sub>:</th><td>' +
            doh +
            '</td><td>m<sup>2</sup>/s</td></tr>' +
            '</table>';
          $('.calculation-result').empty();
          $('.calculation-result').append($new_div);
        }
      });
    } else {
      alert('Please upload excel file');
    }
  });

  $('.button-inibound').click(function () {
    if (uploaded) {
      $xcl_ini = $('.inibound #xcl_ini').val();
      $xf_ini = $('.inibound #xf_ini').val();
      $xoh_ini = $('.inibound #xoh_ini').val();
      $xcl_left = $('.inibound #xcl_left').val();
      $xf_left = $('.inibound #xf_left').val();
      $xoh_left = $('.inibound #xoh_left').val();
      $xcl_right = $('.inibound #xcl_right').val();
      $xf_right = $('.inibound #xf_right').val();
      $xoh_right = $('.inibound #xoh_right').val();

      if (
        $xcl_ini < 0 ||
        $xf_ini < 0 ||
        $xoh_ini < 0 ||
        $xcl_left < 0 ||
        $xf_left < 0 ||
        $xoh_left < 0 ||
        $xcl_right < 0 ||
        $xf_right < 0 ||
        $xoh_right < 0
      ) {
        alert('Input value must > 0');
      } else {
        let sum_ini =
          parseFloat($xcl_ini) + parseFloat($xf_ini) + parseFloat($xoh_ini);
        let sum_left =
          parseFloat($xcl_left) + parseFloat($xf_left) + parseFloat($xoh_left);
        let sum_right =
          parseFloat($xcl_right) +
          parseFloat($xf_right) +
          parseFloat($xoh_right);

        console.log(sum_ini, sum_left, sum_right);
        if (sum_ini <= 1 && sum_left <= 1 && sum_right <= 1) {
          let url = 'https://aptimer.wovodat.org/api/inibound';
          let req_data = {
            xcl_ini: $xcl_ini,
            xf_ini: $xf_ini,
            xoh_ini: $xoh_ini,
            xcl_left: $xcl_left,
            xf_left: $xf_left,
            xoh_left: $xoh_left,
            xcl_right: $xcl_right,
            xf_right: $xf_right,
            xoh_right: $xoh_right,
          };
          $.get(url, req_data, function (data, status) {
            console.log(status);
            console.log(data);
            if (status == 'success') {
              num_plot += 1;
              if (num_plot > 1) {
                num_plot = 1;
                num_run = 0;
              }
              console.log(num_plot);
              var inibound_cl = {
                x: [0, 0, length, length],
                y: data['inibound_cl'],
                type: 'scatter',
                name: 'Initial boundary and conditions',
                line: { color: 'blue', dash: 'dash' },
              };
              var inibound_f = {
                x: [0, 0, length, length],
                y: data['inibound_f'],
                type: 'scatter',
                xaxis: 'x2',
                yaxis: 'y2',
                line: { color: 'blue', dash: 'dash' },
                showlegend: false,
              };
              var inibound_oh = {
                x: [0, 0, length, length],
                y: data['inibound_oh'],
                type: 'scatter',
                xaxis: 'x3',
                yaxis: 'y3',
                line: { color: 'blue', dash: 'dash' },
                showlegend: false,
              };
              var lineCl = {
                x: x,
                y: y_cl,
                error_y: { array: err_cl, visible: true, color: 'black' },
                name: 'Natural data',
                mode: 'lines+markers',
                line: { color: 'black', dash: 'dash', width: 2 },
                type: 'scatter',
              };
              var lineF = {
                x: x,
                y: y_f,
                xaxis: 'x2',
                yaxis: 'y2',
                error_y: { array: err_f, visible: true, color: 'black' },
                mode: 'lines+markers',
                line: { color: 'black', dash: 'dash', width: 2 },
                type: 'scatter',
                showlegend: false,
              };
              var lineOH = {
                x: x,
                y: y_oh,
                xaxis: 'x3',
                yaxis: 'y3',
                error_y: { array: err_oh, visible: true, color: 'black' },
                mode: 'lines+markers',
                line: { color: 'black', dash: 'dash', width: 2 },
                type: 'scatter',
                showlegend: false,
              };
              var layout = {
                grid: { rows: 1, columns: 3, pattern: 'independent' },
                plot_bgcolor: '#ccedff',
                xaxis: { dtick: 2, title: { text: 'Distance (µm)' } },
                xaxis2: { dtick: 2, title: { text: 'Distance (µm)' } },
                xaxis3: { dtick: 2, title: { text: 'Distance (µm)' } },
                yaxis: { dtick: 0.01, title: { text: 'X<sub>Cl</sub>' } },
                yaxis2: { dtick: 0.05, title: { text: 'X<sub>F</sub>' } },
                yaxis3: { dtick: 0.05, title: { text: 'X<sub>OH</sub>' } },
                legend: { orientation: 'h', y: -0.25 },
              };
              Plotly.newPlot(
                'plot',
                [lineCl, lineF, lineOH, inibound_cl, inibound_f, inibound_oh],
                layout
              );
            }
          });
        } else if (sum_ini > 1) {
          alert('Sum of initial condition must <= 1');
        } else if (sum_left > 1) {
          alert('Sum of left boundary must <= 1');
        } else if (sum_right > 1) {
          alert('Sum of right boundary must <= 1');
        }
      }
    } else {
      alert('Please upload excel file');
    }
  });

  $('.button-distime').click(function () {
    if (uploaded) {
      $(this).attr('disabled', true);
      $(this).css('width', '54px');
      $(this).html(
        "<div class='spinner-border' style='width: 1.5rem; height: 1.5rem;' role='status'><span class='sr-only'>Loading...</span></div>"
      );

      $dx = $('.distime #dx').val();
      $dt = $('.distime #dt').val();
      $iteration = $('.distime #iteration').val();

      $temp = $('.diffusivity-cal #temp').val();
      $tilt = $('.diffusivity-cal #tilt').val();

      $xcl_ini = $('.inibound #xcl_ini').val();
      $xf_ini = $('.inibound #xf_ini').val();
      $xoh_ini = $('.inibound #xoh_ini').val();
      $xcl_left = $('.inibound #xcl_left').val();
      $xf_left = $('.inibound #xf_left').val();
      $xoh_left = $('.inibound #xoh_left').val();
      $xcl_right = $('.inibound #xcl_right').val();
      $xf_right = $('.inibound #xf_right').val();
      $xoh_right = $('.inibound #xoh_right').val();

      if ($dx > 1) {
        $('.error-dt').empty();
        $('.error-dt').append(
          '<span style="color: red;">*Check: dx has to be &le; 1!</span>'
        );
        $('.button-distime').removeAttr('disabled');
        $('.button-distime').css('width', '');
        $('.button-distime').html('Run');
      } else {
        let url = 'https://aptimer.wovodat.org/api/distime';
        let req_data = {
          dx: $dx,
          dt: $dt,
          iteration: $iteration,
          length: length,

          temp: $temp,
          tilt: $tilt,

          dcl: dcl,
          df: df,
          doh: doh,

          xcl_ini: $xcl_ini,
          xf_ini: $xf_ini,
          xoh_ini: $xoh_ini,
          xcl_left: $xcl_left,
          xf_left: $xf_left,
          xoh_left: $xoh_left,
          xcl_right: $xcl_right,
          xf_right: $xf_right,
          xoh_right: $xoh_right,

          y_cl: JSON.stringify(y_cl),
          y_f: JSON.stringify(y_f),
          y_oh: JSON.stringify(y_oh),
          err_cl: JSON.stringify(err_cl),
          err_f: JSON.stringify(err_f),
          err_oh: JSON.stringify(err_oh),
        };
        $.get(url, req_data, function (data, status) {
          $('.button-distime').removeAttr('disabled');
          $('.button-distime').css('width', '');
          $('.button-distime').html('Run');

          console.log(status);
          console.log(data);
          if (status == 'success') {
            num_run += 1;
            console.log(num_run);
            let x = data['x'];
            let red_cl = {
              x: x,
              y: data['red_cl'],
              type: 'scatter',
              mode: 'lines',
              name: 'Best-fit line',
              line: { color: 'red' },
            };
            let red_f = {
              x: x,
              y: data['red_f'],
              type: 'scatter',
              mode: 'lines',
              xaxis: 'x2',
              yaxis: 'y2',
              line: { color: 'red' },
              showlegend: false,
            };
            let red_oh = {
              x: x,
              y: data['red_oh'],
              type: 'scatter',
              mode: 'lines',
              xaxis: 'x3',
              yaxis: 'y3',
              line: { color: 'red' },
              showlegend: false,
            };
            let min_cl = {
              x: x,
              y: data['min_Ans'],
              type: 'scatter',
              mode: 'lines',
              name: 'Minimum boundary',
              line: { color: 'green', dash: 'dash' },
            };
            let max_cl = {
              x: x,
              y: data['max_Ans'],
              type: 'scatter',
              mode: 'lines',
              name: 'Maximum boundary',
              line: { color: 'green', dash: 'dash' },
            };

            $('.error-dt').empty();

            if (num_run > 1) {
              Plotly.deleteTraces('plot', [6, 7, 8, 9, 10]);
              Plotly.addTraces('plot', [red_cl, red_f, red_oh, min_cl, max_cl]);
              $new_div =
                "<table class='table table-sm col-lg-6 col-md-8'>" +
                '<tr><th>Best-fit time and uncertainty:</th><td>' +
                data['best_fit_time'] +
                ' (+' +
                data['plus'] +
                '/' +
                data['minus'] +
                ')</td><td> hours</td></tr>' +
                '<tr><th></th><td>~' +
                data['best_day'] +
                '</td><td> days</td></tr>' +
                '</table>';
              $('.model-result').empty();
              $('.model-result').append('<h3>Model fits:</h3>' + $new_div);
            } else {
              Plotly.addTraces('plot', [red_cl, red_f, red_oh, min_cl, max_cl]);
              $new_div =
                "<table class='table table-sm col-lg-6 col-md-8'>" +
                '<tr><th>Best-fit time and uncertainty:</th><td>' +
                data['best_fit_time'] +
                ' (+' +
                data['plus'] +
                '/' +
                data['minus'] +
                ')</td><td> hours</td></tr>' +
                '<tr><th></th><td>~' +
                data['best_day'] +
                '</td><td> days</td></tr>' +
                '</table>';
              $('.model-result').empty();
              $('.model-result').append('<h3>Model fits:</h3>' + $new_div);
            }

            if (data['state'] == 'no best fit')
              $('.model-result').append(
                '<span style="color: red;">No best fit. Please check the input  of dt, dx and iteration.</span>'
              );
          }
        });
      }
    } else {
      alert('Please upload excel file');
    }
  });

  $('.calculate-pt').submit(function (event) {
    event.preventDefault();
    var values = $(this).serialize();
    console.log(values);
    if (values == 'type=transitional') {
      $('#mafic-plot').hide();
      $('#peridotite-plot').hide();
      $('#transitional-plot').show();
      // $('#link').attr('download', 'result-transitional.xlsx');
      // $('#link').attr('href', '../static/result-transitional.xlsx');
    } else if (values == 'type=mafic') {
      $('#transitional-plot').hide();
      $('#peridotite-plot').hide();
      $('#mafic-plot').show();
      // $('#link').attr('download', 'result-mafic.xlsx');
      // $('#link').attr('href', '../static/result-mafic.xlsx');
    } else if (values == 'type=peridotite') {
      $('#transitional-plot').hide();
      $('#mafic-plot').hide();
      $('#peridotite-plot').show();
      // $('#link').attr('download', 'result-peridotite.xlsx');
      // $('#link').attr('href', '../static/result-peridotite.xlsx');
    }
  });

  // $('<img/>')
  //   .on('load', function () {
  //     console.log('good!');
  //     $('#error-text').text('');
  //     $('#image-display').show();
  //   })
  //   .on('error', function () {
  //     console.log('error!');
  //     $('#image-display').hide();
  //     $('#error-text').text('Please upload your excel file');
  //   });
  $('#image-container')
    .imagesLoaded()
    .always(function (instance) {
      // console.log('all images loaded');
      // location.reload();
    })
    .done(function (instance) {
      $('#image-display').show();
      // location.reload();
      $('#error-text').text('');
      console.log('first figure successfully loaded');
    })
    .fail(function () {
      $('#image-display').hide();
      console.log('all images loaded, at least one is broken');
      $('#error-text').text('Please upload your image file');
    })
    .progress(function (instance, image) {
      var result = image.isLoaded ? 'loaded' : 'broken';
      console.log('image is ' + result + ' for ' + image.img.src);
      // location.reload();
    });
  // $('.showbtn').click(function () {
  //   $('.myimgdivshowhide').show();
  // });
  // $('.hidebtn').click(function () {
  //   $('.myimgdivshowhide').hide();
  // });
});
