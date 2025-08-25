import React, { useState } from 'react';
import { submitReview, updateReview } from '../../services/reviewService';

const ReviewForm = ({ treatmentId, existingReview, onSubmit, onCancel }) => {
  const [review, setReview] = useState({
    treatmentId,
    rating: existingReview?.rating || 5,
    effectiveness: existingReview?.effectiveness || 3,
    sideEffects: existingReview?.sideEffects || [],
    sideEffectSeverity: existingReview?.sideEffectSeverity || 1,
    comments: existingReview?.comments || '',
  });
  
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  
  const handleChange = (e) => {
    const { name, value } = e.target;
    setReview(prev => ({ ...prev, [name]: value }));
  };
  
  const handleSideEffectChange = (e) => {
    const { value, checked } = e.target;
    
    setReview(prev => {
      if (checked) {
        return { ...prev, sideEffects: [...prev.sideEffects, value] };
      } else {
        return { ...prev, sideEffects: prev.sideEffects.filter(effect => effect !== value) };
      }
    });
  };
  
  const handleSubmit = async (e) => {
    e.preventDefault();
    
    try {
      setLoading(true);
      setError('');
      
      if (existingReview) {
        await updateReview(treatmentId, review);
      } else {
        await submitReview(review);
      }
      
      onSubmit();
    } catch (err) {
      setError(err.message || 'Failed to submit review. Please try again.');
    } finally {
      setLoading(false);
    }
  };
  
  const commonSideEffects = [
    'Nausea', 'Headache', 'Dizziness', 'Fatigue', 
    'Rash', 'Stomach pain', 'Drowsiness', 'Insomnia'
  ];
  
  return (
    <div className="review-form-container">
      <h3>{existingReview ? 'Update Review' : 'Add Review'}</h3>
      
      {error && <div className="error-message">{error}</div>}
      
      <form onSubmit={handleSubmit} className="review-form">
        <div className="form-group">
          <label>Overall Rating</label>
          <div className="rating-input">
            {[1, 2, 3, 4, 5].map(star => (
              <label key={star} className="star-label">
                <input
                  type="radio"
                  name="rating"
                  value={star}
                  checked={parseInt(review.rating) === star}
                  onChange={handleChange}
                />
                <span className={parseInt(review.rating) >= star ? 'star filled' : 'star'}>
                  ★
                </span>
              </label>
            ))}
          </div>
        </div>
        
        <div className="form-group">
          <label htmlFor="effectiveness">Effectiveness</label>
          <select
            id="effectiveness"
            name="effectiveness"
            value={review.effectiveness}
            onChange={handleChange}
          >
            <option value="1">Not effective</option>
            <option value="2">Slightly effective</option>
            <option value="3">Moderately effective</option>
            <option value="4">Very effective</option>
            <option value="5">Extremely effective</option>
          </select>
        </div>
        
        <div className="form-group">
          <label>Side Effects Experienced</label>
          <div className="side-effects-checkboxes">
            {commonSideEffects.map(effect => (
              <label key={effect} className="checkbox-label">
                <input
                  type="checkbox"
                  name="sideEffects"
                  value={effect}
                  checked={review.sideEffects.includes(effect)}
                  onChange={handleSideEffectChange}
                />
                {effect}
              </label>
            ))}
          </div>
        </div>
        
        {review.sideEffects.length > 0 && (
          <div className="form-group">
            <label htmlFor="sideEffectSeverity">Side Effect Severity</label>
            <select
              id="sideEffectSeverity"
              name="sideEffectSeverity"
              value={review.sideEffectSeverity}
              onChange={handleChange}
            >
              <option value="1">Mild</option>
              <option value="2">Moderate</option>
              <option value="3">Severe</option>
            </select>
          </div>
        )}
        
        <div className="form-group">
          <label htmlFor="comments">Additional Comments</label>
          <textarea
            id="comments"
            name="comments"
            value={review.comments}
            onChange={handleChange}
            rows="4"
            placeholder="Share your experience with this treatment..."
          />
        </div>
        
        <div className="form-buttons">
          <button 
            type="button" 
            onClick={onCancel}
            className="cancel-button"
          >
            Cancel
          </button>
          <button 
            type="submit" 
            className="submit-button"
            disabled={loading}
          >
            {loading ? 'Submitting...' : existingReview ? 'Update Review' : 'Submit Review'}
          </button>
        </div>
      </form>
    </div>
  );
};

export default ReviewForm;
