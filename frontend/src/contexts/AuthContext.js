import React, { createContext, useState, useEffect, useContext } from 'react';

// Create context
const AuthContext = createContext();

// Auth provider component
export const AuthProvider = ({ children }) => {
  const [currentUser, setCurrentUser] = useState(null);
  const [loading, setLoading] = useState(true);
  
  // Mock function to check if user is logged in (replace with actual API calls)
  useEffect(() => {
    const checkLoggedIn = async () => {
      try {
        // Check if token exists in local storage
        const token = localStorage.getItem('token');
        
        if (token) {
          // In a real app, you would verify the token with your backend
          // Mock user data for demo purposes
          const storedUser = JSON.parse(localStorage.getItem('user'));
          setCurrentUser(storedUser);
        }
      } catch (error) {
        console.error('Authentication error:', error);
        localStorage.removeItem('token');
        localStorage.removeItem('user');
      } finally {
        setLoading(false);
      }
    };
    
    checkLoggedIn();
  }, []);
  
  // Mock login function
  const login = async (email, password, role = null) => {
    // In a real app, you'd make an API call to your backend
    // Simulating a successful login for demo
    const mockUser = {
      id: '123',
      name: role === 'doctor' ? 'Dr. Sarah Johnson' : (role === 'admin' ? 'Admin User' : 'John Doe'),
      email: email,
      role: role || 'patient', // Default to patient
      profileImage: null
    };
    
    // Store token and user in local storage
    localStorage.setItem('token', 'mock-jwt-token');
    localStorage.setItem('user', JSON.stringify(mockUser));
    
    setCurrentUser(mockUser);
    return mockUser;
  };
  
  // Mock registration function
  const register = async (userData) => {
    // In a real app, you'd make an API call to your backend
    // Simulating a successful registration for demo
    const mockUser = {
      id: '123',
      name: userData.name || 'New User',
      email: userData.email,
      role: userData.role || 'patient', // Default to patient
      profileImage: null
    };
    
    // Store token and user in local storage
    localStorage.setItem('token', 'mock-jwt-token');
    localStorage.setItem('user', JSON.stringify(mockUser));
    
    setCurrentUser(mockUser);
    return mockUser;
  };
  
  // Logout function
  const logout = () => {
    localStorage.removeItem('token');
    localStorage.removeItem('user');
    setCurrentUser(null);
  };
  
  // Context value
  const value = {
    currentUser,
    loading,
    login,
    register,
    logout,
    isAuthenticated: !!currentUser
  };
  
  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
};

// Custom hook to use the auth context
export const useAuth = () => {
  return useContext(AuthContext);
};
