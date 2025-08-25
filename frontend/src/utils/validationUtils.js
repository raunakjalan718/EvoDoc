/**
 * Utility functions for form validation
 */

// Validate email format
export const isValidEmail = (email) => {
  const regex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return regex.test(email);
};

// Validate password strength
export const isStrongPassword = (password) => {
  // At least 8 characters, one uppercase, one lowercase, one number
  const regex = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).{8,}$/;
  return regex.test(password);
};

// Get password strength feedback
export const getPasswordStrength = (password) => {
  if (!password) return { score: 0, feedback: 'Password is required' };
  
  let score = 0;
  let feedback = '';
  
  if (password.length >= 8) score += 1;
  if (password.length >= 12) score += 1;
  if (/[A-Z]/.test(password)) score += 1;
  if (/[a-z]/.test(password)) score += 1;
  if (/\d/.test(password)) score += 1;
  if (/[^A-Za-z0-9]/.test(password)) score += 1;
  
  switch (true) {
    case (score <= 2):
      feedback = 'Weak: Try using a longer password with symbols and numbers';
      break;
    case (score <= 4):
      feedback = 'Moderate: Consider adding more variety';
      break;
    default:
      feedback = 'Strong password';
  }
  
  return { score, feedback };
};

// Validate phone number format
export const isValidPhoneNumber = (phone) => {
  // Basic validation - can be extended for international formats
  const regex = /^\+?[0-9]{10,15}$/;
  return regex.test(phone.replace(/\s+/g, ''));
};

// Check if all required fields are filled
export const validateRequiredFields = (data, requiredFields) => {
  const errors = {};
  
  requiredFields.forEach(field => {
    if (!data[field]) {
      errors[field] = 'This field is required';
    }
  });
  
  return errors;
};
