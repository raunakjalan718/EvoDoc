import api from './api';

export const getStats = async () => {
  try {
    const response = await api.get('/admin/stats/');
    return response.data;
  } catch (error) {
    throw new Error('Failed to fetch admin statistics');
  }
};

export const getRecentUsers = async (limit = 10) => {
  try {
    const response = await api.get(`/admin/users/recent?limit=${limit}`);
    return response.data;
  } catch (error) {
    throw new Error('Failed to fetch recent users');
  }
};

export const getRecentReviews = async (limit = 10) => {
  try {
    const response = await api.get(`/admin/reviews/recent?limit=${limit}`);
    return response.data;
  } catch (error) {
    throw new Error('Failed to fetch recent reviews');
  }
};

export const getAllUsers = async (page = 1, limit = 20) => {
  try {
    const response = await api.get(`/admin/users?page=${page}&limit=${limit}`);
    return response.data;
  } catch (error) {
    throw new Error('Failed to fetch users');
  }
};

export const getUserDetails = async (userId) => {
  try {
    const response = await api.get(`/admin/users/${userId}`);
    return response.data;
  } catch (error) {
    throw new Error('Failed to fetch user details');
  }
};

export const updateUserStatus = async (userId, status) => {
  try {
    const response = await api.patch(`/admin/users/${userId}/status`, { status });
    return response.data;
  } catch (error) {
    throw new Error('Failed to update user status');
  }
};

export const getDashboardData = async () => {
  try {
    // Make parallel requests for efficiency
    const [stats, users, reviews] = await Promise.all([
      getStats(),
      getRecentUsers(),
      getRecentReviews()
    ]);
    
    return {
      stats,
      recentUsers: users,
      recentReviews: reviews
    };
  } catch (error) {
    throw new Error('Failed to fetch dashboard data');
  }
};
