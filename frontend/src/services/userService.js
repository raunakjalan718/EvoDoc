import api from './api';

export const getUserProfile = async () => {
  try {
    const response = await api.get('/users/me/');
    return response.data;
  } catch (error) {
    throw new Error('Failed to fetch user profile');
  }
};

export const updateUserProfile = async (profileData) => {
  try {
    const response = await api.put('/users/me/', profileData);
    return response.data;
  } catch (error) {
    throw new Error('Failed to update profile');
  }
};

export const getPatients = async () => {
  try {
    const response = await api.get('/doctor/patients/');
    return response.data;
  } catch (error) {
    throw new Error('Failed to fetch patients');
  }
};

export const getPatientById = async (patientId) => {
  try {
    const response = await api.get(`/doctor/patients/${patientId}`);
    return response.data;
  } catch (error) {
    throw new Error('Failed to fetch patient details');
  }
};

export const getDoctors = async () => {
  try {
    const response = await api.get('/users/doctors/');
    return response.data;
  } catch (error) {
    throw new Error('Failed to fetch doctors');
  }
};
