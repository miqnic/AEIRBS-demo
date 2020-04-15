  var ctx = document.getElementById('myChart').getContext('2d');
  var myChart = new Chart(ctx, {
    type: 'line',
    data: {
      labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sept', 'Oct', 'Nov', 'Dec'],
      datasets: [{
        label: 'Earthquake',
        data: [1, 3, 5, 7, 9, 11],
        backgroundColor: [
          'rgb(229, 191, 154, 0.3)',
        ],
        borderColor: [
          'rgb(229, 191, 154)',

        ],
        borderWidth: 3
      }, {
        label: 'Fire',
        data: [4, 23, 10, 12, 10],
        backgroundColor: [
          'rgba(255, 126, 103, 0.3)',
        ],
        borderColor: [
          'rgba(255, 126, 103, 1)',

        ],
        borderWidth: 3
      }, {
        label: 'Flood',
        data: [12, 19, 3, 5, 2, 3],
        backgroundColor: [
          'rgba(162, 213, 242, 0.3)',
        ],
        borderColor: [
          'rgba(162, 213, 242, 1)',
        ],
        borderWidth: 3
      }]
    },
    options: {
      scales: {
        yAxes: [{
          ticks: {
            beginAtZero: true
          }
        }]
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
        backgroundColor: [
          'rgb(229, 191, 154, 0.3)',
          'rgb(229, 191, 154, 0.3)',
          'rgb(229, 191, 154, 0.3)',
          'rgb(229, 191, 154, 0.3)',
          'rgb(229, 191, 154, 0.3)',
          'rgb(229, 191, 154, 0.3)',
          'rgb(229, 191, 154, 0.3)',
          'rgb(229, 191, 154, 0.3)',
          'rgb(229, 191, 154, 0.3)',
          'rgb(229, 191, 154, 0.3)',
          'rgb(229, 191, 154, 0.3)',
        ],
        borderColor: [
          'rgb(229, 191, 154, 1)',

        ],
        borderWidth: 1
      }]
    },
    options: {
      scales: {
        yAxes: [{
          ticks: {
            beginAtZero: true
          }
        }]
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
        backgroundColor: [
          'rgba(255, 126, 103, 0.3)',
          'rgba(255, 126, 103, 0.3)',
          'rgba(255, 126, 103, 0.3)',
          'rgba(255, 126, 103, 0.3)',
          'rgba(255, 126, 103, 0.3)',
          'rgba(255, 126, 103, 0.3)',
          'rgba(255, 126, 103, 0.3)',
          'rgba(255, 126, 103, 0.3)',
          'rgba(255, 126, 103, 0.3)',
          'rgba(255, 126, 103, 0.3)',
          'rgba(255, 126, 103, 0.3)',
          'rgba(255, 126, 103, 0.3)',
          'rgba(255, 126, 103, 0.3)',
        ],
        borderColor: [
          'rgba(255, 126, 103, 1)',
          'rgba(255, 126, 103, 1)',
          'rgba(255, 126, 103, 1)',
          'rgba(255, 126, 103, 1)',
          'rgba(255, 126, 103, 1)',
          'rgba(255, 126, 103, 1)',
          'rgba(255, 126, 103, 1)',
          'rgba(255, 126, 103, 1)',
          'rgba(255, 126, 103, 1)',
          'rgba(255, 126, 103, 1)',
          'rgba(255, 126, 103, 1)',
          'rgba(255, 126, 103, 1)',
        ],
        borderWidth: 1
      }]
    },
    options: {
      scales: {
        yAxes: [{
          ticks: {
            beginAtZero: true
          }
        }]
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
        backgroundColor: [
          'rgba(162, 213, 242, 0.3)',
          'rgba(162, 213, 242, 0.3)',
          'rgba(162, 213, 242, 0.3)',
          'rgba(162, 213, 242, 0.3)',
          'rgba(162, 213, 242, 0.3)',
          'rgba(162, 213, 242, 0.3)',
          'rgba(162, 213, 242, 0.3)',
          'rgba(162, 213, 242, 0.3)',
          'rgba(162, 213, 242, 0.3)',
          'rgba(162, 213, 242, 0.3)',
          'rgba(162, 213, 242, 0.3)',
          'rgba(162, 213, 242, 0.3)',
        ],
        borderColor: [
          'rgba(162, 213, 242, 1)',
          'rgba(162, 213, 242, 1)',
          'rgba(162, 213, 242, 1)',
          'rgba(162, 213, 242, 1)',
          'rgba(162, 213, 242, 1)',
          'rgba(162, 213, 242, 1)',
          'rgba(162, 213, 242, 1)',
          'rgba(162, 213, 242, 1)',
          'rgba(162, 213, 242, 1)',
          'rgba(162, 213, 242, 1)',
          'rgba(162, 213, 242, 1)',
          'rgba(162, 213, 242, 1)',
        ],
        borderWidth: 1
      }]
    },
    options: {
      scales: {
        yAxes: [{
          ticks: {
            beginAtZero: true
          }
        }]
      }
    }
  });

