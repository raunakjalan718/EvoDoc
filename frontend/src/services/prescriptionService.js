import api from './api';

export const createPrescription = async (prescriptionData) => {
  try {
    const response = await api.post('/doctor/prescriptions/', prescriptionData);
    return response.data;
  } catch (error) {
    throw new Error('Failed to create prescription');
  }
};

export const getPrescriptionById = async (prescriptionId) => {
  try {
    const response = await api.get(`/prescriptions/${prescriptionId}`);
    return response.data;
  } catch (error) {
    throw new Error('Failed to fetch prescription details');
  }
};

export const getPatientPrescriptions = async () => {
  try {
    const response = await api.get('/patient/prescriptions/');
    return response.data;
  } catch (error) {
    throw new Error('Failed to fetch patient prescriptions');
  }
};

export const getDoctorPrescriptions = async () => {
  try {
    const response = await api.get('/doctor/prescriptions/');
    return response.data;
  } catch (error) {
    throw new Error('Failed to fetch doctor prescriptions');
  }
};

export const updatePrescriptionStatus = async (prescriptionId, status) => {
  try {
    const response = await api.patch(`/prescriptions/${prescriptionId}`, { status });
    return response.data;
  } catch (error) {
    throw new Error('Failed to update prescription status');
  }
};
