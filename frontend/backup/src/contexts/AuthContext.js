import React, { createContext, useState, useContext, useEffect } from 'react';
import axios from 'axios';
import { jwtDecode } from 'jwt-decode';

// Define API URL
const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000/api/v1';

// Create a basic API service inline (to avoid the module not found error)
const authAPI = {
  login: (username, password) => 
    axios.post(`${API_URL}/token/`, { username, password }),
  
  register: (userData) => 
    axios.post(`${API_URL}/register/`, userData),
  
  getCurrentUser: () => {
    const token = localStorage.getItem('token');
    return axios.get(`${API_URL}/users/me/`, {
      headers: { Authorization: `Bearer ${token}` }
    });
  }
};

const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
  const [currentUser, setCurrentUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // Check if we have a token on mount
  useEffect(() => {
    const checkLoggedIn = async () => {
      try {
        const token = localStorage.getItem('token');
        if (token) {
          // Check if token is expired
          const decoded = jwtDecode(token);
          const currentTime = Date.now() / 1000;
          if (decoded.exp < currentTime) {
            localStorage.removeItem('token');
            localStorage.removeItem('refreshToken');
            setCurrentUser(null);
          } else {
            const response = await authAPI.getCurrentUser();
            setCurrentUser(response.data);
          }
        }
      } catch (err) {
        console.error("Authentication error:", err);
        localStorage.removeItem('token');
        localStorage.removeItem('refreshToken');
      } finally {
        setLoading(false);
      }
    };

    checkLoggedIn();
  }, []);

  const login = async (username, password) => {
    try {
      setError(null);
      const response = await authAPI.login(username, password);
      localStorage.setItem('token', response.data.access);
      localStorage.setItem('refreshToken', response.data.refresh);
      
      // Get user details
      const userResponse = await authAPI.getCurrentUser();
      setCurrentUser(userResponse.data);
      return userResponse.data;
    } catch (err) {
      setError(err.response?.data?.detail || 'Login failed');
      throw err;
    }
  };

  const register = async (userData) => {
    try {
      setError(null);
      await authAPI.register(userData);
      return await login(userData.username, userData.password);
    } catch (err) {
      setError(err.response?.data || 'Registration failed');
      throw err;
    }
  };

  const logout = () => {
    localStorage.removeItem('token');
    localStorage.removeItem('refreshToken');
    setCurrentUser(null);
  };

  return (
    <AuthContext.Provider value={{
      currentUser,
      loading,
      error,
      login,
      register,
      logout,
      isAuthenticated: !!currentUser,
      isPatient: currentUser?.user_type === 'patient',
      isDoctor: currentUser?.user_type === 'doctor',
    }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => useContext(AuthContext);
