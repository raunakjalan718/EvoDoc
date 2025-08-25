import React from 'react';

/**
 * Reusable icon button component
 */
const IconButton = ({
  icon,
  onClick,
  label,
  variant = 'default',
  size = 'medium',
  disabled = false,
  className = '',
  ...props
}) => {
  // Base classes
  const baseClasses = 'inline-flex items-center justify-center rounded-full focus:outline-none transition-colors duration-200';
  
  // Size classes
  const sizeClasses = {
    small: 'p-1.5',
    medium: 'p-2',
    large: 'p-3',
  };
  
  // Icon size classes
  const iconSizeClasses = {
    small: 'w-4 h-4',
    medium: 'w-5 h-5',
    large: 'w-6 h-6',
  };
  
  // Variant classes
  const variantClasses = {
    default: 'text-gray-600 hover:text-gray-900 hover:bg-gray-100',
    primary: 'text-primary-600 hover:text-primary-700 hover:bg-primary-50',
    secondary: 'text-gray-500 hover:text-gray-700 hover:bg-gray-100',
    danger: 'text-red-600 hover:text-red-700 hover:bg-red-50',
    transparent: 'text-current hover:bg-gray-100 bg-transparent',
  };
  
  // Disabled class
  const disabledClass = disabled ? 'opacity-50 cursor-not-allowed' : '';
  
  // Combine all classes
  const buttonClasses = `
    ${baseClasses}
    ${sizeClasses[size] || sizeClasses.medium}
    ${variantClasses[variant] || variantClasses.default}
    ${disabledClass}
    ${className}
  `;
  
  return (
    <button
      type="button"
      className={buttonClasses}
      onClick={onClick}
      disabled={disabled}
      aria-label={label}
      title={label}
      {...props}
    >
      {React.isValidElement(icon) ? (
        React.cloneElement(icon, {
          className: `${iconSizeClasses[size] || iconSizeClasses.medium} ${icon.props.className || ''}`,
        })
      ) : (
        <span className={iconSizeClasses[size] || iconSizeClasses.medium}>{icon}</span>
      )}
    </button>
  );
};

export default IconButton;
