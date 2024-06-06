import axios from 'axios';
import jwt_decode from 'jwt-decode';
import { v4 as uuidv4 } from 'uuid';
import fs from 'fs';
import path from 'path';
import sendActivityData from './sendActivityData';

// Define the threshold for the activity data size
const THRESHOLD = 500000; // 0.5 MB

// Create an instance of Axios
const api = axios.create();

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
  const activityData = [
    requestId,
    endpoint + "/" + httpMethod,
    query,
    httpMethod,
    pricingPlan,
    requestSize,
    response.status,
    requestTime,
    JSON.stringify(response.data).length,
    concurrentUsers,
    Boolean(isCached),
    startTime,
  ].join(',') + '\n';

  if (process.env.NODE_ENV === 'production') {
    // Retrieve the existing CSV data from the user's session
    const existingActivityData = window.sessionStorage.getItem('activityData') || '';
  
    // Append the new CSV data to the existing CSV data
    const newActivityData = existingActivityData + activityData;
  
    // Store the new CSV data in the user's session
    window.sessionStorage.setItem('activityData', newActivityData);

    // If the activityData surpasses a certain threshold, send it to the backend
    if (newActivityData.length > THRESHOLD) {
      sendActivityData(newActivityData);
    }
  }
  else if (typeof process.env.NODE_ENV === 'undefined'){}
  else {  
    const path = require('path');

    // Get the path to the project's root directory
    const rootPath = path.resolve(__dirname, '..');
    
    // Append the path to the machine-learning folder
    const filePath = path.resolve(rootPath, 'machine-learning/training/dataset/frontend_access_data.csv');
  
    // Check if file exists, if not, write headers
    if (!fs.existsSync(filePath)) {
      fs.writeFileSync(filePath, 'Request ID,Endpoint,Query,HTTP method,Pricing Plan,Request Size,Response Status,Round-trip Time,Response Size,Concurrent Users,Cache Used,Request Time\n');
    }
  
    // Append the data to the CSV file
    fs.appendFileSync(filePath, activityData);
  }

  return response;
}, (error) => {
  const urlConfig = new URL(error.config.url);
  const endpoint = urlConfig.origin + urlConfig.pathname;
  activeRequests[endpoint]--;
  return Promise.reject(error);
});