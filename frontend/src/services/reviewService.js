import api from './api';

export const submitReview = async (reviewData) => {
  try {
    const response = await api.post('/reviews/', reviewData);
    return response.data;
  } catch (error) {
    throw new Error('Failed to submit review');
  }
};

export const updateReview = async (reviewId, reviewData) => {
  try {
    const response = await api.put(`/reviews/${reviewId}`, reviewData);
    return response.data;
  } catch (error) {
    throw new Error('Failed to update review');
  }
};

export const getReviewById = async (reviewId) => {
  try {
    const response = await api.get(`/reviews/${reviewId}`);
    return response.data;
  } catch (error) {
    throw new Error('Failed to fetch review');
  }
};

export const getReviewsForTreatment = async (treatmentId) => {
  try {
    const response = await api.get(`/patient-treatments/${treatmentId}/reviews`);
    return response.data;
  } catch (error) {
    throw new Error('Failed to fetch reviews for treatment');
  }
};

export const getPatientReviews = async () => {
  try {
    const response = await api.get('/reviews/');
    return response.data;
  } catch (error) {
    throw new Error('Failed to fetch patient reviews');
  }
};
