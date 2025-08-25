import React from 'react';

/**
 * Reusable button component with multiple variants
 */
const Button = ({
  children,
  variant = 'primary',
  size = 'medium',
  type = 'button',
  fullWidth = false,
  disabled = false,
  onClick,
  className = '',
  ...props
}) => {
  // Base button classes
  const baseClasses = 'font-medium rounded focus:outline-none transition-all duration-200';
  
  // Size classes
  const sizeClasses = {
    small: 'px-3 py-1 text-sm',
    medium: 'px-4 py-2',
    large: 'px-6 py-3 text-lg',
  };
  
  // Variant classes
  const variantClasses = {
    primary: 'bg-primary-600 hover:bg-primary-700 text-white shadow-sm',
    secondary: 'bg-gray-200 hover:bg-gray-300 text-gray-800',
    outline: 'border border-primary-600 text-primary-600 hover:bg-primary-50',
    danger: 'bg-red-600 hover:bg-red-700 text-white',
    success: 'bg-green-600 hover:bg-green-700 text-white',
  };
  
  // Disabled classes
  const disabledClasses = disabled 
    ? 'opacity-50 cursor-not-allowed' 
    : 'hover:shadow';
    
  // Width classes
  const widthClasses = fullWidth ? 'w-full' : '';
  
  // Combine all classes
  const buttonClasses = `
    ${baseClasses} 
    ${sizeClasses[size] || sizeClasses.medium} 
    ${variantClasses[variant] || variantClasses.primary}
    ${disabledClasses}
    ${widthClasses}
    ${className}
  `;

  return (
    <button
      type={type}
      className={buttonClasses}
      disabled={disabled}
      onClick={onClick}
      {...props}
    >
      {children}
    </button>
  );
};

export default Button;
