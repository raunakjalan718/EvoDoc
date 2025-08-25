import React, { useState, useEffect } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import { getPatientById } from '../../services/userService';
import { getMedications } from '../../services/medicationService';
import { createPrescription } from '../../services/prescriptionService';

const Prescribe = () => {
  const location = useLocation();
  const navigate = useNavigate();
  const queryParams = new URLSearchParams(location.search);
  const patientId = queryParams.get('patientId');
  
  const [patient, setPatient] = useState(null);
  const [medications, setMedications] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  
  const [prescription, setPrescription] = useState({
    patientId: patientId || '',
    medicationId: '',
    dosage: '',
    frequency: '',
    duration: '',
    instructions: '',
    startDate: new Date().toISOString().split('T')[0],
  });
  
  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true);
        
        // Fetch medications
        const medsData = await getMedications();
        setMedications(medsData);
        
        // If patientId exists, fetch patient details
        if (patientId) {
          const patientData = await getPatientById(patientId);
          setPatient(patientData);
          setPrescription(prev => ({
            ...prev,
            patientId
          }));
        }
      } catch (err) {
        setError('Failed to load data. Please try again later.');
        console.error(err);
      } finally {
        setLoading(false);
      }
    };
    
    fetchData();
  }, [patientId]);
  
  const handleChange = (e) => {
    const { name, value } = e.target;
    setPrescription(prev => ({ ...prev, [name]: value }));
  };
  
  const handleSubmit = async (e) => {
    e.preventDefault();
    
    try {
      setLoading(true);
      setError('');
      setSuccess('');
      
      await createPrescription(prescription);
      setSuccess('Prescription created successfully!');
      
      // Reset form
      setPrescription({
        patientId: patientId || '',
        medicationId: '',
        dosage: '',
        frequency: '',
        duration: '',
        instructions: '',
        startDate: new Date().toISOString().split('T')[0],
      });
      
      // Redirect after a delay
      setTimeout(() => {
        navigate('/doctor/patients');
      }, 2000);
    } catch (err) {
      setError(err.message || 'Failed to create prescription. Please try again.');
    } finally {
      setLoading(false);
    }
  };
  
  if (loading && !medications.length) {
    return <div className="loading-spinner">Loading...</div>;
  }
  
  return (
    <div className="prescribe-page">
      <h1>Create Prescription</h1>
      
      {error && <div className="error-message">{error}</div>}
      {success && <div className="success-message">{success}</div>}
      
      {patient && (
        <div className="patient-info-card">
          <h2>Patient Information</h2>
          <p><strong>Name:</strong> {patient.firstName} {patient.lastName}</p>
          <p><strong>Age:</strong> {patient.age || 'Not specified'}</p>
          <p><strong>Allergies:</strong> {patient.allergies || 'None reported'}</p>
        </div>
      )}
      
      <form onSubmit={handleSubmit} className="prescription-form">
        {!patient && (
          <div className="form-group">
            <label htmlFor="patientId">Patient</label>
            <select
              id="patientId"
              name="patientId"
              value={prescription.patientId}
              onChange={handleChange}
              required
            >
              <option value="">Select a patient</option>
              {/* In a real app, you'd fetch patients here */}
              <option value="1">John Doe</option>
              <option value="2">Jane Smith</option>
            </select>
          </div>
        )}
        
        <div className="form-group">
          <label htmlFor="medicationId">Medication</label>
          <select
            id="medicationId"
            name="medicationId"
            value={prescription.medicationId}
            onChange={handleChange}
            required
          >
            <option value="">Select a medication</option>
            {medications.map(med => (
              <option key={med.id} value={med.id}>
                {med.name} ({med.dosageForm}, {med.strength})
              </option>
            ))}
          </select>
        </div>
        
        <div className="form-row">
          <div className="form-group">
            <label htmlFor="dosage">Dosage</label>
            <input
              type="text"
              id="dosage"
              name="dosage"
              value={prescription.dosage}
              onChange={handleChange}
              placeholder="e.g., 1 tablet"
              required
            />
          </div>
          
          <div className="form-group">
            <label htmlFor="frequency">Frequency</label>
            <input
              type="text"
              id="frequency"
              name="frequency"
              value={prescription.frequency}
              onChange={handleChange}
              placeholder="e.g., twice daily"
              required
            />
          </div>
        </div>
        
        <div className="form-row">
          <div className="form-group">
            <label htmlFor="duration">Duration</label>
            <input
              type="text"
              id="duration"
              name="duration"
              value={prescription.duration}
              onChange={handleChange}
              placeholder="e.g., 7 days"
              required
            />
          </div>
          
          <div className="form-group">
            <label htmlFor="startDate">Start Date</label>
            <input
              type="date"
              id="startDate"
              name="startDate"
              value={prescription.startDate}
              onChange={handleChange}
              required
            />
          </div>
        </div>
        
        <div className="form-group">
          <label htmlFor="instructions">Special Instructions</label>
          <textarea
            id="instructions"
            name="instructions"
            value={prescription.instructions}
            onChange={handleChange}
            placeholder="Any special instructions for taking this medication"
            rows="4"
          />
        </div>
        
        <button 
          type="submit" 
          className="create-prescription-button"
          disabled={loading}
        >
          {loading ? 'Creating...' : 'Create Prescription'}
        </button>
      </form>
    </div>
  );
};

export default Prescribe;
