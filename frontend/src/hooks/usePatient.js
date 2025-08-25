// src/hooks/usePatient.js
import { useState, useEffect } from 'react';
import api from '../services/api';

export function usePatient(patientId) {
  const [patient, setPatient] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    async function fetchPatient() {
      try {
        setLoading(true);
        const response = await api.get(`/patients/${patientId}/`);
        setPatient(response.data);
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    }

    fetchPatient();
  }, [patientId]);

  return { patient, loading, error };
}
