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
    metrics.map(metric => {
      // Replace dashes with slashes in the endpoint name
      const endpoint = metric.endpoint.replace(/-/g, '/');
      return [
        endpoint,
        metric.complexity,
        metric.duplicity,
        metric.loc
      ].join(',');
    }).join('\n') + '\n';

    // Write the CSV data to a file
    const path = require('path');

    // Get the path to the project's root directory
    const rootPath = path.resolve(__dirname, '..');
    
    // Append the path to the machine-learning folder
    const filePath = path.resolve(rootPath, 'machine-learning/dataset/metrics.csv');
    
    fs.writeFileSync(filePath, csvData);
  }).catch(error => {
    console.error('Error retrieving metrics:', error);
  });
}