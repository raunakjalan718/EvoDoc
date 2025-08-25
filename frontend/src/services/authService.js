import api from './api';

export const loginUser = async (credentials) => {
  try {
    const response = await api.post('/token/', credentials);
    const { access, refresh } = response.data;
    
    // Store tokens in localStorage
    localStorage.setItem('token', access);
    localStorage.setItem('refreshToken', refresh);
    
    return response.data;
  } catch (error) {
    throw new Error(error.response?.data?.detail || 'Login failed');
  }
};

export const registerUser = async (userData) => {
  try {
    const response = await api.post('/register/', userData);
    return response.data;
  } catch (error) {
    throw new Error(error.response?.data?.detail || 'Registration failed');
  }
};

export const logoutUser = () => {
  localStorage.removeItem('token');
  localStorage.removeItem('refreshToken');
  localStorage.removeItem('userRole');
};

export const checkAuthStatus = async () => {
  try {
    const token = localStorage.getItem('token');
    
    if (!token) {
      return { isAuthenticated: false };
    }
    
    // Verify token by making a request to the current user endpoint
    const response = await api.get('/users/me/');
    
    // Store user role for role-based auth
    localStorage.setItem('userRole', response.data.user_type);
    
    return {
      isAuthenticated: true,
      user: response.data
    };
  } catch (error) {
    localStorage.removeItem('token');
    localStorage.removeItem('refreshToken');
    localStorage.removeItem('userRole');
    
    return { isAuthenticated: false };
  }
};
