import api from './api';

export const getTreatments = async () => {
  try {
    const response = await api.get('/patient-treatments/');
    return response.data;
  } catch (error) {
    throw new Error('Failed to fetch treatments');
  }
};

export const getTreatmentById = async (treatmentId) => {
  try {
    const response = await api.get(`/patient-treatments/${treatmentId}`);
    return response.data;
  } catch (error) {
    throw new Error('Failed to fetch treatment details');
  }
};

export const createTreatment = async (treatmentData) => {
  try {
    const response = await api.post('/patient-treatments/', treatmentData);
    return response.data;
  } catch (error) {
    throw new Error('Failed to create treatment');
  }
};

export const updateTreatment = async (treatmentId, treatmentData) => {
  try {
    const response = await api.put(`/patient-treatments/${treatmentId}`, treatmentData);
    return response.data;
  } catch (error) {
    throw new Error('Failed to update treatment');
  }
};

export const deleteTreatment = async (treatmentId) => {
  try {
    await api.delete(`/patient-treatments/${treatmentId}`);
    return true;
  } catch (error) {
    throw new Error('Failed to delete treatment');
  }
};
