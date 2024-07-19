// cpuchart.js

// Load the Google Charts library
google.charts.load('current', {'packages':['corechart']});

// Set a callback to run when the Google Visualization API is loaded.
google.charts.setOnLoadCallback(initializeChart);

let chart;
let data;

function initializeChart() {
    data = new google.visualization.DataTable();
    data.addColumn('datetime', 'Time');
    data.addColumn('number', 'CPU Utilization (%)');

    const options = {
        title: 'CPU Utilization',
        curveType: 'function',
        legend: { position: 'bottom' },
        hAxis: {
            title: 'Time',
            format: 'HH:mm:ss'
        },
        vAxis: {
            title: 'CPU Utilization (%)',
            minValue: 0,
            maxValue: 100
        }
    };

    chart = new google.visualization.LineChart(document.getElementById('cpu-utilization-card'));
    drawChart(); // Initial draw with options

    // Fetch data initially
    fetchCpuUtilization();
    
    // Set interval to fetch data every 5 seconds
    setInterval(fetchCpuUtilization, 5000);
}

// Function to draw the chart with current data and options
function drawChart() {
    chart.draw(data, {
        title: 'CPU Utilization',
        curveType: 'function',
        legend: { position: 'bottom' },
        hAxis: {
            title: 'Time',
            format: 'HH:mm:ss'
        },
        vAxis: {
            title: 'CPU Utilization (%)',
            minValue: 0,
            maxValue: 100
        }
    });
}

// Function to fetch CPU utilization data
function fetchCpuUtilization() {
    $.get('/cpu_utilization', function(response) {
        if (response.status === 'success') {
            const currentTime = new Date();
            data.addRow([currentTime, response.cpu_util]);
            drawChart(); // Redraw chart with updated data
        }
    });
}
