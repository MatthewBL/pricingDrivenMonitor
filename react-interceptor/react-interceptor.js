import { v4 as uuidv4 } from 'uuid';

var successful = true;
var url;
var query;
var httpMethod;
var pricingPlan;
var requestSize;
var responseStatus;
var requestTime;
var responseSize;
var requestId;

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

  // Generate a unique identifier for the request
  requestId = uuidv4();

  // Add the identifier to the request headers
  config.headers['X-Request-ID'] = requestId;

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
    requestId,
    url,
    query,
    httpMethod,
    pricingPlan,
    requestSize,
    responseStatus,
    requestTime,
    responseSize
  ].join(',') + '\n';

  const filePath = path.resolve(__dirname, '../database/frontend_access_data.csv');

  // Check if file exists, if not, write headers
  if (!fs.existsSync(filePath)) {
    fs.writeFileSync(filePath, 'Request ID,URL,Query,HTTP method,Pricing Plan,Request Size,Response Status,Request Time,Response Size\n');
  }

  // Append the data to the CSV file
  fs.appendFileSync(filePath, csvData);
} else {
  console.error('Failed to register interceptors');
}