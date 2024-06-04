import { v4 as uuidv4 } from 'uuid';

let activeRequests = {};

// Add a request interceptor
api.interceptors.request.use((config) => {
  // Create a URL object from the config URL
  const urlConfig = new URL(config.url);

  const endpoint = urlConfig.origin + urlConfig.pathname;
  // Print the base URL
  console.log('Endpoint:', endpoint);

  // Increment the number of active requests for the endpoint
  activeRequests[endpoint] = (activeRequests[endpoint] || 0) + 1;

  const query = urlConfig.search;
  // Print the query parameters
  console.log('Query parameters:', query);

  const httpMethod = config.method.toUpperCase();
  // Print the type of HTTP method
  console.log('HTTP method:', httpMethod);

  // Decode the JWT from the Authorization header
  const token = config.headers.Authorization.split(' ')[1];
  const decodedToken = jwt_decode(token);

  const pricingPlan = decodedToken.pricingPlan;
  // Log the user's pricing plan
  console.log('User pricing plan:', pricingPlan);

  // Calculate the size of the request
  const requestSize = JSON.stringify(config.data).length;
  console.log('Request size:', requestSize, 'bytes');

  // Generate a unique identifier for the request
  const requestId = uuidv4();

  // Add the identifier to the request headers
  config.headers['X-Request-ID'] = requestId;

  // Attach the data to the config object
  config.metadata = {
    requestId,
    endpoint,
    query,
    httpMethod,
    pricingPlan,
    requestSize,
    concurrentUsers: activeRequests[endpoint],
    startTime: new Date()
  };

  return config;
}, (error) => {
  successful = false;
  activeRequests[endpoint]--;
  return Promise.reject(error);
});

// Add a response interceptor
api.interceptors.response.use((response) => {
  // Retrieve the data from the config object
  const { requestId, endpoint, query, httpMethod, pricingPlan, requestSize, startTime, concurrentUsers } = response.config.metadata;

  activeRequests[endpoint]--;
  // Print the HTTP status of the response
  const responseStatus = response.status;
  console.log('Response status:', responseStatus);

  // Check for cache usage
  const cacheControl = response.headers['cache-control'];
  const eTag = response.headers.etag;
  const expires = response.headers.expires;
  const lastModified = response.headers['last-modified'];
  const age = response.headers.age;

  const isCached = cacheControl || eTag || expires || lastModified || age;
  console.log('Cache used:', Boolean(isCached));

  // Calculate the time it took to process the request
  const requestTime = new Date() - startTime;
  console.log('Request processing time:', requestTime, 'ms');

  // Calculate the size of the response
  const responseSize = JSON.stringify(response.data).length;
  console.log('Response size:', responseSize, 'bytes');

  // Format the data as CSV
  const csvData = [
    requestId,
    endpoint + " " + httpMethod,
    query,
    httpMethod,
    pricingPlan,
    requestSize,
    response.status,
    requestTime,
    JSON.stringify(response.data).length,
    concurrentUsers,
    Boolean(isCached),
  ].join(',') + '\n';
  
  const filePath = path.resolve(__dirname, '../machine-learning/frontend_access_data.csv');

  // Check if file exists, if not, write headers
  if (!fs.existsSync(filePath)) {
    fs.writeFileSync(filePath, 'Request ID,Endpoint,Query,HTTP method,Pricing Plan,Request Size,Response Status,Request Time,Response Size,Concurrent Users,Cache Used\n');
  }

  // Append the data to the CSV file
  fs.appendFileSync(filePath, csvData);

  return response;
}, (error) => {
  successful = false;
  const urlConfig = new URL(error.config.url);
  const endpoint = urlConfig.origin + urlConfig.pathname;
  activeRequests[endpoint]--;
  return Promise.reject(error);
});