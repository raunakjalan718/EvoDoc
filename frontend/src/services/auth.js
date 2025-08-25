import axios from 'axios';
import jwt_decode from 'jwt-decode';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

// Create axios instance
const api = axios.create({
  baseURL: `${API_URL}/api`
});

// Add token to requests if available
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('accessToken');
    if (token) {
      config.headers['Authorization'] = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Handle token refresh on 401 errors
api.interceptors.response.use(
  (response) => {
    return response;
  },
  async (error) => {
    const originalRequest = error.config;
    
    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;
      
      try {
        const refreshToken = localStorage.getItem('refreshToken');
        if (!refreshToken) {
          // No refresh token available, need to log in again
          localStorage.removeItem('accessToken');
          localStorage.removeItem('refreshToken');
          localStorage.removeItem('user');
          window.location.href = '/login';
          return Promise.reject(error);
        }
        
        // Try to get new tokens
        const response = await axios.post(`${API_URL}/api/auth/token/refresh/`, {
          refresh: refreshToken
        });
        
        // Store new tokens
        localStorage.setItem('accessToken', response.data.access);
        
        // Update authorization header
        originalRequest.headers['Authorization'] = `Bearer ${response.data.access}`;
        
        // Retry the original request
        return api(originalRequest);
      } catch (refreshError) {
        // Refresh token failed, need to log in again
        localStorage.removeItem('accessToken');
        localStorage.removeItem('refreshToken');
        localStorage.removeItem('user');
        window.location.href = '/login';
        return Promise.reject(refreshError);
      }
    }
    
    return Promise.reject(error);
  }
);

// Auth service functions
const AuthService = {
  register: async (userData) => {
    try {
      const response = await api.post('/auth/register/', userData);
      
      if (response.data.tokens) {
        localStorage.setItem('accessToken', response.data.tokens.access);
        localStorage.setItem('refreshToken', response.data.tokens.refresh);
        localStorage.setItem('user', JSON.stringify(response.data.user));
      }
      
      return response.data;
    } catch (error) {
      throw error.response?.data || { message: 'An error occurred during registration' };
    }
  },
  
  login: async (email, password) => {
    try {
      const response = await api.post('/auth/token/', {
        email,
        password
      });
      
      localStorage.setItem('accessToken', response.data.access);
      localStorage.setItem('refreshToken', response.data.refresh);
      
      // Get user data
      const userData = await AuthService.getCurrentUser();
      localStorage.setItem('user', JSON.stringify(userData));
      
      return userData;
    } catch (error) {
      throw error.response?.data || { message: 'Invalid credentials' };
    }
  },
  
  logout: () => {
    localStorage.removeItem('accessToken');
    localStorage.removeItem('refreshToken');
    localStorage.removeItem('user');
  },
  
  getCurrentUser: async () => {
    try {
      const response = await api.get('/auth/profile/');
      return response.data;
    } catch (error) {
      throw error.response?.data || { message: 'Failed to get user profile' };
    }
  },
  
  isLoggedIn: () => {
    const token = localStorage.getItem('accessToken');
    if (!token) return false;
    
    try {
      // Check if token is expired
      const decoded = jwt_decode(token);
      return decoded.exp * 1000 > Date.now();
    } catch (e) {
      return false;
    }
  },

  hasRole: (role) => {
    const user = JSON.parse(localStorage.getItem('user'));
    return user && user.user_type === role;
  },
  
  verifyEmail: async (uidb64, token) => {
    try {
      const response = await api.get(`/auth/verify-email/${uidb64}/${token}/`);
      return response.data;
    } catch (error) {
      throw error.response?.data || { message: 'Failed to verify email' };
    }
  },
  
  updateProfile: async (profileData) => {
    try {
      const response = await api.patch('/auth/profile/', profileData);
      
      // Update user in localStorage
      const currentUser = JSON.parse(localStorage.getItem('user'));
      const updatedUser = { ...currentUser, ...response.data };
      localStorage.setItem('user', JSON.stringify(updatedUser));
      
      return updatedUser;
    } catch (error) {
      throw error.response?.data || { message: 'Failed to update profile' };
    }
  },
  
  requestPasswordReset: async (email) => {
    try {
      const response = await api.post('/auth/password-reset/', { email });
      return response.data;
    } catch (error) {
      throw error.response?.data || { message: 'Failed to request password reset' };
    }
  },
  
  resetPassword: async (uidb64, token, password, password_confirm) => {
    try {
      const response = await api.post(`/auth/password-reset/${uidb64}/${token}/`, {
        password,
        password_confirm
      });
      return response.data;
    } catch (error) {
      throw error.response?.data || { message: 'Failed to reset password' };
    }
  },
  
  deactivateAccount: async () => {
    try {
      const response = await api.post('/auth/deactivate/');
      return response.data;
    } catch (error) {
      throw error.response?.data || { message: 'Failed to deactivate account' };
    }
  },
  
  // Admin-specific functions
  activateAccount: async (userId) => {
    try {
      const response = await api.post(`/auth/activate/${userId}/`);
      return response.data;
    } catch (error) {
      throw error.response?.data || { message: 'Failed to activate account' };
    }
  },
  
  approveDoctor: async (userId) => {
    try {
      const response = await api.post(`/auth/doctors/approve/${userId}/`);
      return response.data;
    } catch (error) {
      throw error.response?.data || { message: 'Failed to approve doctor' };
    }
  },
  
  getUserList: async (filters = {}) => {
    try {
      // Convert filters object to query string
      const queryParams = new URLSearchParams(filters).toString();
      const response = await api.get(`/auth/users/?${queryParams}`);
      return response.data;
    } catch (error) {
      throw error.response?.data || { message: 'Failed to get user list' };
    }
  }
};

export default AuthService;
