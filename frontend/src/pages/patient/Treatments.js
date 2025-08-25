import React, { useState, useEffect } from 'react';
import { getTreatments } from '../../services/treatmentService';
import TreatmentCard from '../../components/treatment/TreatmentCard';

const Treatments = () => {
  const [treatments, setTreatments] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  
  useEffect(() => {
    const fetchTreatments = async () => {
      try {
        const data = await getTreatments();
        setTreatments(data);
      } catch (err) {
        setError('Failed to load treatments. Please try again later.');
        console.error(err);
      } finally {
        setLoading(false);
      }
    };
    
    fetchTreatments();
  }, []);
  
  if (loading) return <div className="loading-spinner">Loading treatments...</div>;
  
  return (
    <div className="treatments-page">
      <h1>My Treatments</h1>
      
      {error && <div className="error-message">{error}</div>}
      
      {treatments.length === 0 ? (
        <div className="no-treatments">
          <p>You don't have any treatments yet.</p>
        </div>
      ) : (
        <div className="treatments-grid">
          {treatments.map(treatment => (
            <TreatmentCard 
              key={treatment.id} 
              treatment={treatment}
            />
          ))}
        </div>
      )}
    </div>
  );
};

export default Treatments;
