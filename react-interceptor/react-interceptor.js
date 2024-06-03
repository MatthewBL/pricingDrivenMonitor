var successful = true;
var url;
var query;
var httpMethod;
var pricingPlan;
var requestSize;
var responseStatus;
var requestTime;
var responseSize;

// Add a request interceptor
api.interceptors.request.use((config) => {
  // Create a URL object from the config URL
  const urlConfig = new URL(config.url);

  url = urlConfig.origin + urlConfig.pathname;
  // Print the base URL
  console.log('Base URL:', url);

  query = urlConfig.search;
  // Print the query parameters
  console.log('Query parameters:', query);

  httpMethod = config.method.toUpperCase();
  // Print the type of HTTP method
  console.log('HTTP method:', httpMethod);

  // Decode the JWT from the Authorization header
  const token = config.headers.Authorization.split(' ')[1];
  const decodedToken = jwt_decode(token);

  pricingPlan = decodedToken.pricingPlan;
  // Log the user's pricing plan
  console.log('User pricing plan:', pricingPlan);

  // Calculate the size of the request
  requestSize = JSON.stringify(config.data).length;
  console.log('Request size:', requestSize, 'bytes');

  // Add a timestamp to the config
  config.metadata = { startTime: new Date() };

  return config;
}, (error) => {
  successful = false;
  return Promise.reject(error);
});

// Add a response interceptor
api.interceptors.response.use((response) => {
  // Print the HTTP status of the response
  responseStatus = response.status;
  console.log('Response status:', responseStatus);

  // Calculate the time it took to process the request
  requestTime = new Date() - response.config.metadata.startTime;
  console.log('Request processing time:', requestTime, 'ms');

  // Calculate the size of the response
  responseSize = JSON.stringify(response.data).length;
  console.log('Response size:', responseSize, 'bytes');

  return response;
}, (error) => {
  successful = false;
  return Promise.reject(error);
});

if (successful) {
  console.log('Interceptors registered successfully');

  // Format the data as CSV
  const csvData = [
    url,
    query,
    httpMethod,
    pricingPlan,
    requestSize,
    responseStatus,
    requestTime,
    responseSize
  ].join(',') + '\n';

  // Append the data to the CSV file
  fs.appendFileSync(path.resolve(__dirname, '../database/frontend_access_data.csv'), csvData);
} else {
  console.error('Failed to register interceptors');
}