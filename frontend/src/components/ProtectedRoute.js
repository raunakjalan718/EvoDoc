import React from 'react';
import { Navigate, useLocation } from 'react-router-dom';
import { useSelector } from 'react-redux';

/**
 * Component to protect routes based on authentication and role
 * @param {Object} props
 * @param {React.ReactNode} props.children - The components to render if authorized
 * @param {string} [props.requiredRole] - Optional role required to access the route
 * @param {string} [props.redirectPath] - Path to redirect to if unauthorized (defaults to /login)
 */
const ProtectedRoute = ({ 
  children, 
  requiredRole,
  redirectPath = '/login'
}) => {
  const { isLoggedIn, user, isLoading } = useSelector(state => state.auth);
  const location = useLocation();

  // Show loading indicator while auth state is being determined
  if (isLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
      </div>
    );
  }

  // If not logged in, redirect to login with return path
  if (!isLoggedIn) {
    return (
      <Navigate 
        to={redirectPath} 
        state={{ from: location.pathname }}
        replace
      />
    );
  }

  // Check if user is verified when required
  if (requiredRole && !user.is_verified) {
    return (
      <Navigate 
        to="/verify-email-required" 
        replace
      />
    );
  }

  // Check if user has required role
  if (requiredRole && user.user_type !== requiredRole) {
    // Handle different role redirects
    if (user.user_type === 'patient') {
      return <Navigate to="/patient/dashboard" replace />;
    } else if (user.user_type === 'doctor') {
      return <Navigate to="/doctor/dashboard" replace />;
    } else if (user.user_type === 'admin') {
      return <Navigate to="/admin/dashboard" replace />;
    }
    
    // Default fallback
    return <Navigate to="/" replace />;
  }

  // If doctor, check if approved when accessing doctor routes
  if (user.user_type === 'doctor' && requiredRole === 'doctor' && !user.is_approved) {
    return (
      <Navigate 
        to="/doctor/approval-pending" 
        replace
      />
    );
  }

  // If everything checks out, render the protected component
  return children;
};

export default ProtectedRoute;
