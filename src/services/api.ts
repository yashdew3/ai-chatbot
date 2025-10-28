import axios from 'axios';

// Create an Axios instance configured to talk to your backend
const apiClient = axios.create({
  // Environment-based configuration for production deployment
  baseURL: import.meta.env.VITE_API_URL || 'https://ai-chatbot-api-n1vm.onrender.com',
  headers: {
    'Content-Type': 'application/json',
  },
});

// You can add interceptors here later for handling auth tokens automatically

export default apiClient;