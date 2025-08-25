import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { getPatients } from '../../services/userService';

const Patients = () => {
  const [patients, setPatients] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [searchTerm, setSearchTerm] = useState('');
  
  useEffect(() => {
    const fetchPatients = async () => {
      try {
        const data = await getPatients();
        setPatients(data);
      } catch (err) {
        setError('Failed to load patients. Please try again later.');
        console.error(err);
      } finally {
        setLoading(false);
      }
    };
    
    fetchPatients();
  }, []);
  
  const filteredPatients = patients.filter(patient => {
    const fullName = `${patient.firstName} ${patient.lastName}`.toLowerCase();
    return fullName.includes(searchTerm.toLowerCase());
  });
  
  if (loading) return <div className="loading-spinner">Loading patients...</div>;
  
  return (
    <div className="patients-page">
      <h1>My Patients</h1>
      
      {error && <div className="error-message">{error}</div>}
      
      <div className="search-container">
        <input
          type="text"
          placeholder="Search patients..."
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
          className="search-input"
        />
      </div>
      
      {filteredPatients.length === 0 ? (
        <div className="no-patients">
          <p>No patients found.</p>
        </div>
      ) : (
        <div className="patients-table-container">
          <table className="patients-table">
            <thead>
              <tr>
                <th>Name</th>
                <th>Age</th>
                <th>Last Visit</th>
                <th>Conditions</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              {filteredPatients.map(patient => (
                <tr key={patient.id}>
                  <td>
                    <div className="patient-name">
                      {patient.firstName} {patient.lastName}
                    </div>
                  </td>
                  <td>{patient.age || '-'}</td>
                  <td>{patient.lastVisit || 'Never'}</td>
                  <td>
                    <div className="conditions-list">
                      {patient.conditions?.map((condition, index) => (
                        <span key={index} className="condition-badge">
                          {condition}
                        </span>
                      )) || '-'}
                    </div>
                  </td>
                  <td>
                    <div className="actions-cell">
                      <Link 
                        to={`/doctor/patients/${patient.id}`} 
                        className="view-button"
                      >
                        View
                      </Link>
                      <Link 
                        to={`/doctor/prescribe?patientId=${patient.id}`} 
                        className="prescribe-button"
                      >
                        Prescribe
                      </Link>
                    </div>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
};

export default Patients;
