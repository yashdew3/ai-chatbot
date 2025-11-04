import axios from 'axios';

// Production API Client - Uses environment variable for backend URL
const apiClient = axios.create({
  // Use environment variable in production, fallback to localhost for development
  baseURL: import.meta.env.VITE_BACKEND_URL || 'http://localhost:8000',
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 60000, // 60 second timeout for AI responses
});

// Add request interceptor for debugging
apiClient.interceptors.request.use(
  (config) => {
    console.log('🚀 API Request:', config.method?.toUpperCase(), config.url);
    console.log('🌐 Backend URL:', config.baseURL);
    return config;
  },
  (error) => {
    console.error('❌ API Request Error:', error);
    return Promise.reject(error);
  }
);

// Add response interceptor for debugging and error handling
apiClient.interceptors.response.use(
  (response) => {
    console.log('✅ API Response:', response.status, response.config.url);
    return response;
  },
  (error) => {
    console.error('❌ API Response Error:', error.message);
    
    if (error.code === 'ECONNREFUSED' || error.code === 'ENOTFOUND') {
      console.error('🔥 Backend connection failed! Check if backend is running.');
    } else if (error.code === 'ECONNABORTED') {
      console.error('⏱️ Request timeout - AI response took too long');
    }
    
    return Promise.reject(error);
  }
);

export default apiClient;