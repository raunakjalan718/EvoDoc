import React from 'react';
import { Navigate, useLocation } from 'react-router-dom';
import { useAuth } from '../../contexts/AuthContext';
import Loader from '../common/Loader';

/**
 * Protected route component for restricting access based on authentication and role
 */
const ProtectedRoute = ({ 
  children, 
  requiredRole,
  redirectPath = '/login'
}) => {
  const { isAuthenticated, loading, user } = useAuth();
  const location = useLocation();

  // Show loader while checking authentication
  if (loading) {
    return <Loader.FullPage message="Checking authentication..." />;
  }

  // If not authenticated, redirect to login with return path
  if (!isAuthenticated) {
    return (
      <Navigate 
        to={redirectPath} 
        state={{ from: location.pathname }}
        replace
      />
    );
  }

  // If role is required and user doesn't have it, redirect to home
  if (requiredRole && user.role !== requiredRole) {
    return <Navigate to="/" replace />;
  }

  // If authenticated and has required role, render the protected component
  return children;
};

export default ProtectedRoute;
