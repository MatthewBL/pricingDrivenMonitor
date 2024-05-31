import axios from 'axios';

// Create an axios instance
const api = axios.create();

// Add a request interceptor
api.interceptors.request.use((config) => {
  // Do something before request is sent
  console.log('Calling endpoint:', config.url);
  return config;
}, (error) => {
  // Do something with request error
  return Promise.reject(error);
});

// Add a response interceptor
api.interceptors.response.use((response) => {
  // Do something with response data
  console.log('Response received at:', new Date().toISOString());
  return response;
}, (error) => {
  // Do something with response error
  return Promise.reject(error);
});

export default api;