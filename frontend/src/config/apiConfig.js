/**
 * API configuration
 */

// Base API URL
export const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000/api/v1';

// API endpoints
export const API_ENDPOINTS = {
  // Auth
  LOGIN: '/token/',
  REFRESH_TOKEN: '/token/refresh/',
  REGISTER: '/register/',
  CURRENT_USER: '/users/me/',
  
  // Users
  USERS: '/users/',
  DOCTORS: '/users/doctors/',
  
  // Patient
  PATIENT_PROFILE: '/patient/profile/',
  PATIENT_TREATMENTS: '/patient-treatments/',
  PATIENT_MEDICATIONS: '/patient-medications/',
  PATIENT_CONDITIONS: '/patient-conditions/',
  
  // Doctor
  DOCTOR_PROFILE: '/doctor/profile/',
  DOCTOR_PATIENTS: '/doctor/patients/',
  DOCTOR_PRESCRIPTIONS: '/doctor/prescriptions/',
  
  // Treatments
  TREATMENTS: '/treatments/',
  
  // Reviews
  REVIEWS: '/reviews/',
  
  // Medications
  MEDICATIONS: '/medications/',
  
  // Conditions
  CONDITIONS: '/conditions/',
  
  // Admin
  ADMIN_STATS: '/admin/stats/',
  ADMIN_USERS: '/admin/users/',
  ADMIN_REVIEWS: '/admin/reviews/',
};

// Request timeout in milliseconds
export const REQUEST_TIMEOUT = 30000;

// Number of retry attempts for failed requests
export const RETRY_ATTEMPTS = 3;
