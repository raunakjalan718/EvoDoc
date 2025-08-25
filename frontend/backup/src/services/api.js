// src/services/api.js - Create this file after fixing the current errors
import axios from 'axios';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000/api/v1';

// Create axios instance
const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  }
});

// Add token to request if available
api.interceptors.request.use(
  config => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  error => Promise.reject(error)
);

// Auth APIs
export const authAPI = {
  login: (username, password) => api.post('/token/', { username, password }),
  register: (userData) => api.post('/register/', userData),
  getCurrentUser: () => api.get('/users/me/'),
};

export default api;
