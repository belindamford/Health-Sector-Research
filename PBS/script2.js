
// Include Plotly.js library in your HTML file
<script src="https://cdn.plot.ly/plotly-latest.min.js"></script>

// JavaScript to create the bar chart
function createChart(processedData) {
  const trace1 = {
    x: processedData.map((_, index) => `Data ${index + 1}`),
    y: processedData.map(d => d.fy24All),
    name: 'FY24 All',
    type: 'bar'
  };

  const trace2 = {
    x: processedData.map((_, index) => `Data ${index + 1}`),
    y: processedData.map(d => d.fy24Change),
    name: 'FY24 Change',
    type: 'bar'
  };

  const data = [trace1, trace2];

  const layout = {
    barmode: 'group',
    title: 'FY24 All and FY24 Change Data',
    xaxis: { title: 'Data Points' },
    yaxis: { title: 'Values' }
  };

  Plotly.newPlot('chartDiv', data, layout);
}
Papa.parse('path/to/your/PBS_all_fin_year.csv', {
  header: true,
  download: true,
  complete: function(results) {
    const data = results.data;
    const processedData = processData(data);
    createChart(processedData);
  }
});
