import { useState, useEffect, useCallback } from 'react';
import api from '../services/api';

/**
 * Custom hook for fetching data from API
 * @param {string} url - API endpoint to fetch from
 * @param {Object} options - Fetch options
 * @returns {Object} - Data, loading state, error, and refetch function
 */
const useFetch = (url, options = {}) => {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  
  // Function to fetch data that can be called again if needed
  const fetchData = useCallback(async () => {
    setLoading(true);
    setError(null);
    
    try {
      const response = await api.get(url, options);
      setData(response.data);
    } catch (err) {
      setError(err.message || 'An error occurred while fetching data');
      console.error(`Error fetching data from ${url}:`, err);
    } finally {
      setLoading(false);
    }
  }, [url, options]);
  
  // Fetch data on mount and when dependencies change
  useEffect(() => {
    fetchData();
  }, [fetchData]);
  
  // Return data, loading state, error, and refetch function
  return { data, loading, error, refetch: fetchData };
};

export default useFetch;
