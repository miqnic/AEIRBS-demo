  var ctx = document.getElementById('myChart').getContext('2d');
  var myChart = new Chart(ctx, {
    type: 'line',
    data: {
      labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sept', 'Oct', 'Nov', 'Dec'],
      datasets: [{
        label: 'Earthquake',
        data: [1, 3, 5, 7, 9, 11], 
        lineTension: 0,
        backgroundColor: 'rgb(229, 191, 154, 0.3)',
        borderColor: 'rgb(229, 191, 154)',
        borderWidth: 3,
        pointBorderColor: 'rgb(229, 191, 154)',
        pointBackgroundColor: 'rgb(229, 191, 154, 0.8)',
        pointRadius: 3,
        pointHoverBackgroundColor: 'rgb(254, 193, 7)',
        pointHoverBorderColor: 'rgb(254, 193, 7)',
        pointHoverRadius: 5,
      }, {
        label: 'Fire',
        data: [4, 23, 10, 12, 10],
        lineTension: 0,
        backgroundColor: 'rgba(255, 126, 103, 0.3)',
        borderColor: 'rgba(255, 126, 103)',
        borderWidth: 3,
        pointBorderColor: 'rgba(255, 126, 103)',
        pointBackgroundColor: 'rgba(255, 126, 103, 0.8)',
        pointRadius: 3,
        pointHoverBackgroundColor: 'rgb(254, 193, 7)',
        pointHoverBorderColor: 'rgb(254, 193, 7)',
        pointHoverRadius: 5,
      }, {
        label: 'Flood',
        data: [12, 19, 3, 5, 2, 3],
        lineTension: 0,
        lineTension: 0,
          backgroundColor: 'rgba(162, 213, 242, 0.3)',
          borderColor: 'rgba(162, 213, 242)',
          borderWidth: 3,
          pointBorderColor: 'rgba(162, 213, 242)',
          pointBackgroundColor: 'rgba(162, 213, 242, 0.8)',
          pointRadius: 3,
          pointHoverBackgroundColor: 'rgb(254, 193, 7)',
          pointHoverBorderColor: 'rgb(254, 193, 7)',
          pointHoverRadius: 5,
      }]
    },
    options: {
      scales: {
        yAxes: [{
          scaleLabel: {
            display: true,
            labelString: 'Number of Occurrence',
            fontFamily: 'Montserrat',
            fontStyle: 'bold',
          }
        }],
        xAxes: [{
          scaleLabel: {
            display: true,
            labelString: 'Month',
            fontFamily: 'Montserrat',
            fontStyle: 'bold',
          }
        }],
      }
    }
  });

  var ctx1 = document.getElementById('myChart1').getContext('2d');
  var myChart1 = new Chart(ctx1, {
    type: 'bar',
    data: {
      labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sept', 'Oct', 'Nov', 'Dec'],
      datasets: [{
        label: 'Earthquake',
        data: [12, 19, 3, 5, 2, 3],
        backgroundColor:'rgb(229, 191, 154, 0.3)',
        borderColor:'rgb(229, 191, 154, 1)',
        borderWidth: 3
      }]
    },
    options: {
      scales: {
        yAxes: [{
          scaleLabel: {
            display: true,
            labelString: 'Y Label',
            fontFamily: 'Montserrat',
            fontSize: 8,
            fontStyle: 'bold',
          }
        }],
        xAxes: [{
          scaleLabel: {
            display: true,
            labelString: 'X Label',
            fontFamily: 'Montserrat',
            fontSize: 8,
            fontStyle: 'bold',
          }
        }],
      }
    }
  });

  var ctx2 = document.getElementById('myChart2').getContext('2d');
  var myChart2 = new Chart(ctx2, {
    type: 'bar',
    data: {
      labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sept', 'Oct', 'Nov', 'Dec'],
      datasets: [{
        label: 'Fire',
        data: [12, 19, 3, 5, 2, 3],
        backgroundColor:'rgba(255, 126, 103, 0.3)',
        borderColor:'rgba(255, 126, 103, 1)',
        borderWidth: 3
      }]
    },
    options: {
      scales: {
        yAxes: [{
          scaleLabel: {
            display: true,
            labelString: 'Y Label',
            fontFamily: 'Montserrat',
            fontSize: 8,
            fontStyle: 'bold',
          }
        }],
        xAxes: [{
          scaleLabel: {
            display: true,
            labelString: 'X Label',
            fontFamily: 'Montserrat',
            fontSize: 8,
            fontStyle: 'bold',
          }
        }],
      }
    }
  });

  var ctx3 = document.getElementById('myChart3').getContext('2d');
  var myChart3 = new Chart(ctx3, {
    type: 'bar',
    data: {
      labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sept', 'Oct', 'Nov', 'Dec'],
      datasets: [{
        label: 'Flood',
        data: [12, 19, 3, 5, 2, 3],
        backgroundColor:'rgba(162, 213, 242, 0.3)',
        borderColor:'rgba(162, 213, 242, 1)',
        borderWidth: 3
      }]
    },
    options: {
      scales: {
        yAxes: [{
          scaleLabel: {
            display: true,
            labelString: 'Y Label',
            fontFamily: 'Montserrat',
            fontSize: 8,
            fontStyle: 'bold',
          }
        }],
        xAxes: [{
          scaleLabel: {
            display: true,
            labelString: 'X Label',
            fontFamily: 'Montserrat',
            fontSize: 8,
            fontStyle: 'bold',
          }
        }],
      }
    }
  });
