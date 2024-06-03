const axios = require('axios');
const fs = require('fs');
const path = require('path');

function fetchAndWriteMetrics(apiToken, projectId) {
  axios.get(`https://api.codacy.com/2.0/project/${projectId}/metrics`, {
    headers: {
      'api_token': apiToken
    }
  }).then(response => {
    const metrics = response.data;

    // Format the metrics as CSV
    const csvData = [
      'Endpoint',
      'Cyclomatic Complexity',
      'Code Duplicity',
      'Lines of Code'
    ].join(',') + '\n' +
    metrics.map(metric => [
      metric.endpoint,
      metric.complexity,
      metric.duplicity,
      metric.loc
    ].join(',')).join('\n') + '\n';

    // Write the CSV data to a file
    fs.writeFileSync(path.resolve(__dirname, '../database/metrics.csv'), csvData);
  }).catch(error => {
    console.error('Error retrieving metrics:', error);
  });
}