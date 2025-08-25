/**
 * Utility functions for formatting data
 */

// Format currency
export const formatCurrency = (amount, currency = 'USD') => {
  return new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency: currency,
  }).format(amount);
};

// Capitalize first letter of each word
export const capitalizeWords = (str) => {
  if (!str) return '';
  return str
    .split(' ')
    .map(word => word.charAt(0).toUpperCase() + word.slice(1).toLowerCase())
    .join(' ');
};

// Format medication dosage
export const formatDosage = (dosage, dosageForm) => {
  if (!dosage) return '';
  
  if (dosageForm) {
    return `${dosage} ${dosageForm}`;
  }
  
  return dosage;
};

// Format treatment duration
export const formatDuration = (duration) => {
  if (!duration) return '';
  
  const durationNum = parseInt(duration);
  if (isNaN(durationNum)) return duration;
  
  if (durationNum === 1) {
    return '1 day';
  } else if (durationNum < 7) {
    return `${durationNum} days`;
  } else if (durationNum % 7 === 0) {
    const weeks = durationNum / 7;
    return `${weeks} ${weeks === 1 ? 'week' : 'weeks'}`;
  } else if (durationNum % 30 === 0) {
    const months = durationNum / 30;
    return `${months} ${months === 1 ? 'month' : 'months'}`;
  }
  
  return `${durationNum} days`;
};

// Truncate text with ellipsis
export const truncateText = (text, maxLength = 100) => {
  if (!text || text.length <= maxLength) return text;
  return text.slice(0, maxLength) + '...';
};

// Format name (first initial of last name)
export const formatDoctorName = (firstName, lastName) => {
  if (!firstName || !lastName) return '';
  return `Dr. ${firstName} ${lastName.charAt(0)}.`;
};
