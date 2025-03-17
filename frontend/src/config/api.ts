import axios from 'axios';

// Use environment variable for API URL, with fallback for local development
// @ts-ignore - Ignore TypeScript error for env property
const apiUrl = import.meta.env.VITE_API_URL || 'http://localhost:8001';

console.log('API URL:', apiUrl); // Debug log

const api = axios.create({
  baseURL: apiUrl,
  headers: {
    'Content-Type': 'application/json',
  },
  withCredentials: false, // Set to false to avoid CORS preflight issues
});

// Add request interceptor to include auth token
api.interceptors.request.use(
  (config) => {
    console.log(`Making ${config.method?.toUpperCase()} request to ${config.baseURL}${config.url}`);
    console.log('Request headers:', config.headers);
    console.log('Request data:', config.data);
    
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    console.error('Request error:', error);
    return Promise.reject(error);
  }
);

// Add response interceptor for better error handling
api.interceptors.response.use(
  (response) => {
    console.log('Response received:', response.status);
    console.log('Response data:', response.data);
    return response;
  },
  (error) => {
    console.error('Response error:', error.response?.status, error.response?.data || error.message);
    if (error.response) {
      console.error('Error response headers:', error.response.headers);
    }
    return Promise.reject(error);
  }
);

export default api;
