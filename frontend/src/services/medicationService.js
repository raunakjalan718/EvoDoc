import api from './api';

export const getMedications = async () => {
  try {
    const response = await api.get('/medications/');
    return response.data;
  } catch (error) {
    throw new Error('Failed to fetch medications');
  }
};

export const getMedicationById = async (medicationId) => {
  try {
    const response = await api.get(`/medications/${medicationId}`);
    return response.data;
  } catch (error) {
    throw new Error('Failed to fetch medication details');
  }
};

export const searchMedications = async (query) => {
  try {
    const response = await api.get(`/medications/search?q=${query}`);
    return response.data;
  } catch (error) {
    throw new Error('Failed to search medications');
  }
};

export const getPatientMedications = async () => {
  try {
    const response = await api.get('/patient-medications/');
    return response.data;
  } catch (error) {
    throw new Error('Failed to fetch patient medications');
  }
};
