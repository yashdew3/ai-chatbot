import axios from 'axios';

// Create an Axios instance configured to talk to your backend
const apiClient = axios.create({
  // Environment-based configuration for production deployment
  baseURL: import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000',
  headers: {
    'Content-Type': 'application/json',
  },
});

// You can add interceptors here later for handling auth tokens automatically

export default apiClient;