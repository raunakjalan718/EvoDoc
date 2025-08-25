import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import ReviewForm from '../review/ReviewForm';

const TreatmentCard = ({ treatment }) => {
  const [showReviewForm, setShowReviewForm] = useState(false);
  
  const toggleReviewForm = () => {
    setShowReviewForm(!showReviewForm);
  };
  
  const handleReviewSubmit = () => {
    setShowReviewForm(false);
    // In a real app, you might refresh the treatment data here
  };
  
  return (
    <div className="treatment-card">
      <div className="treatment-header">
        <h2>{treatment.name}</h2>
        <span className={`status-badge ${treatment.status}`}>
          {treatment.status}
        </span>
      </div>
      
      <div className="treatment-body">
        <p className="prescribed-by">
          Prescribed by Dr. {treatment.prescribedBy}
        </p>
        
        <div className="treatment-dates">
          <p>
            <strong>Start Date:</strong> {treatment.startDate}
          </p>
          {treatment.endDate && (
            <p>
              <strong>End Date:</strong> {treatment.endDate}
            </p>
          )}
        </div>
        
        <div className="medications-list">
          <h3>Medications</h3>
          <ul>
            {treatment.medications.map((medication, index) => (
              <li key={index}>
                <div className="medication-item">
                  <span className="medication-name">{medication.name}</span>
                  <span className="medication-details">
                    {medication.dosage}, {medication.frequency}
                  </span>
                </div>
              </li>
            ))}
          </ul>
        </div>
        
        {treatment.notes && (
          <div className="treatment-notes">
            <h3>Notes</h3>
            <p>{treatment.notes}</p>
          </div>
        )}
      </div>
      
      <div className="treatment-footer">
        <Link 
          to={`/patient/treatments/${treatment.id}`} 
          className="view-details-button"
        >
          View Details
        </Link>
        
        <button 
          onClick={toggleReviewForm} 
          className="add-review-button"
        >
          {treatment.hasReview ? 'Update Review' : 'Add Review'}
        </button>
      </div>
      
      {showReviewForm && (
        <ReviewForm 
          treatmentId={treatment.id} 
          existingReview={treatment.review}
          onSubmit={handleReviewSubmit}
          onCancel={toggleReviewForm}
        />
      )}
    </div>
  );
};

export default TreatmentCard;
