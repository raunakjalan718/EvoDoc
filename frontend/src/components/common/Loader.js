import React from 'react';

/**
 * Reusable loader component
 */
const Loader = ({ size = 'medium', color = 'primary', className = '' }) => {
  // Size classes
  const sizeClasses = {
    small: 'w-4 h-4 border-2',
    medium: 'w-8 h-8 border-3',
    large: 'w-12 h-12 border-4',
  };
  
  // Color classes
  const colorClasses = {
    primary: 'border-primary-200 border-t-primary-600',
    secondary: 'border-gray-200 border-t-gray-600',
    white: 'border-gray-100 border-t-white',
  };
  
  const loaderSizeClass = sizeClasses[size] || sizeClasses.medium;
  const loaderColorClass = colorClasses[color] || colorClasses.primary;

  return (
    <div className={`inline-block ${className}`}>
      <div 
        className={`rounded-full animate-spin ${loaderSizeClass} ${loaderColorClass}`}
        role="status"
      >
        <span className="sr-only">Loading...</span>
      </div>
    </div>
  );
};

/**
 * Full page loader with overlay
 */
Loader.FullPage = function FullPageLoader({ message = 'Loading...' }) {
  return (
    <div className="fixed inset-0 bg-white bg-opacity-75 flex flex-col items-center justify-center z-50">
      <Loader size="large" />
      {message && <p className="mt-4 text-gray-700 text-lg">{message}</p>}
    </div>
  );
};

export default Loader;
