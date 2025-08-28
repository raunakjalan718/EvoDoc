import os
import numpy as np
import pandas as pd
import pickle
from typing import List, Dict, Tuple, Any

# Paths
MODEL_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "models")
TRAINED_DIR = os.path.join(MODEL_DIR, "trained")
FEATURE_DIR = os.path.join(MODEL_DIR, "feature_extractors")

class MedicationRecommender:
    """Treatment recommendation model"""
    
    def __init__(self):
        """Initialize model"""
        # Load feature extractor
        with open(os.path.join(FEATURE_DIR, "patient_feature_extractor.pkl"), 'rb') as f:
            self.feature_extractor = pickle.load(f)
        
        # Load best model
        with open(os.path.join(TRAINED_DIR, "best_recommendation_model.pkl"), 'rb') as f:
            self.model = pickle.load(f)
        
        # Load medication data
        self.medications = pd.read_csv(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 
                                                 "data", "synthetic", "medications.csv"))
        
        # Load medication ingredients mapping
        med_ingredients = pd.read_csv(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 
                                                 "data", "synthetic", "medication_ingredient.csv"))
        
        # Load ingredients
        ingredients = pd.read_csv(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 
                                              "data", "synthetic", "ingredients.csv"))
        
        # Merge to get medication ingredients
        self.med_ingredients = pd.merge(
            med_ingredients,
            ingredients[['id', 'name']],
            left_on='ingredient_id',
            right_on='id',
            how='inner'
        )
        
        # Load allergy ingredient mapping
        allergy_ingredients = pd.read_csv(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 
                                                       "data", "synthetic", "allergy_ingredient.csv"))
        
        # Merge to get allergy ingredients
        self.allergy_ingredients = pd.merge(
            allergy_ingredients,
            ingredients[['id', 'name']],
            left_on='ingredient_id',
            right_on='id',
            how='inner'
        )
        
    def check_allergies(self, medication_id: int, patient_allergies: List[int]) -> List[Dict]:
        """Check if medication has ingredients that the patient is allergic to
        
        Args:
            medication_id: Medication ID
            patient_allergies: List of allergy IDs
            
        Returns:
            List of dictionaries with allergy information
        """
        contraindications = []
        
        # Get medication ingredients
        med_ingredients = self.med_ingredients[self.med_ingredients['medication_id'] == medication_id]
        
        for _, ingredient in med_ingredients.iterrows():
            # Check if ingredient is in allergies
            for allergy_id in patient_allergies:
                allergy_ingredients = self.allergy_ingredients[self.allergy_ingredients['allergy_id'] == allergy_id]
                
                if ingredient['ingredient_id'] in allergy_ingredients['ingredient_id'].values:
                    contraindications.append({
                        'medication_id': medication_id,
                        'ingredient_id': ingredient['ingredient_id'],
                        'ingredient_name': ingredient['name'],
                        'allergy_id': allergy_id
                    })
        
        return contraindications
        
    def recommend(self, patient_data: Dict, patient_allergies: List[int] = None) -> Dict:
        """Recommend treatments based on patient data
        
        Args:
            patient_data: Dictionary with patient information
                - age: int
                - gender: str
                - diagnosis: str
                - medications: List[str]
            patient_allergies: List of allergy IDs
                
        Returns:
            Dictionary with recommendations
        """
        # Extract features
        X = self.feature_extractor.transform_patient(patient_data)
        
        # Get all medication names
        all_medications = self.medications['name'].unique()
        
        # Predict effectiveness for each medication
        predictions = []
        
        for medication in all_medications:
            # Update patient data with this medication
            patient_data_copy = patient_data.copy()
            patient_data_copy['medications'] = [medication]
            
            # Extract features
            X_med = self.feature_extractor.transform_patient(patient_data_copy)
            
            # Predict effectiveness
            effectiveness = self.model.predict(X_med)[0]
            
            predictions.append({
                'medication': medication,
                'medication_id': self.medications[self.medications['name'] == medication]['id'].iloc[0],
                'effectiveness': effectiveness,
                'confidence': min(1.0, max(0.0, effectiveness + 0.2))  # Simple confidence calculation
            })
        
        # Sort by effectiveness
        predictions.sort(key=lambda x: x['effectiveness'], reverse=True)
        
        # Check for allergies
        contraindications = []
        alternatives = []
        safe_treatments = []
        
        if patient_allergies:
            for pred in predictions:
                # Check allergies
                med_allergies = self.check_allergies(pred['medication_id'], patient_allergies)
                
                if med_allergies:
                    # Add to contraindications
                    for allergy in med_allergies:
                        contraindications.append({
                            'medication': pred['medication'],
                            'ingredient': allergy['ingredient_name'],
                            'reason': f"Patient is allergic to {allergy['ingredient_name']}"
                        })
                else:
                    # Add to safe treatments
                    safe_treatments.append(pred)
            
            # Find alternatives for contraindicated medications
            for contra in contraindications:
                # Find alternative with similar effectiveness
                for safe in safe_treatments[:3]:  # Consider top 3 safe treatments
                    alternatives.append({
                        'original': contra['medication'],
                        'alternative': safe['medication'],
                        'reason': contra['reason']
                    })
        else:
            # No allergies, all treatments are safe
            safe_treatments = predictions
        
        # Limit to top 5 recommendations
        recommendations = safe_treatments[:5] if len(safe_treatments) > 0 else predictions[:5]
        
        return {
            'recommendations': recommendations,
            'contraindications': contraindications,
            'alternatives': alternatives[:3] if alternatives else [],
            'explanation': f"Based on patient profile and diagnosis. Top recommendation has {recommendations[0]['confidence']:.0%} confidence."
        }

class SideEffectPredictor:
    """Side effect prediction model"""
    
    def __init__(self):
        """Initialize model"""
        # Load models
        with open(os.path.join(TRAINED_DIR, "side_effect_severity_model.pkl"), 'rb') as f:
            self.severity_model = pickle.load(f)
            
        with open(os.path.join(TRAINED_DIR, "side_effect_frequency_model.pkl"), 'rb') as f:
            self.frequency_model = pickle.load(f)
            
        # Load medication encoder
        with open(os.path.join(TRAINED_DIR, "medication_encoder.pkl"), 'rb') as f:
            self.medication_encoder = pickle.load(f)
            
        # Load side effects
        self.side_effects = pd.read_csv(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 
                                                    "data", "synthetic", "side_effects.csv"))
        
        # Load medications
        self.medications = pd.read_csv(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 
                                                   "data", "synthetic", "medications.csv"))
    
    def predict_side_effects(self, medication_name: str, patient_data: Dict = None) -> List[Dict]:
        """Predict side effects for a medication
        
        Args:
            medication_name: Name of the medication
            patient_data: Dictionary with patient information (optional)
                - age: int
                - gender: str
                
        Returns:
            List of dictionaries with side effect predictions
        """
        # Get medication ID
        try:
            medication_id = self.medications[self.medications['name'] == medication_name]['id'].iloc[0]
        except IndexError:
            return []
            
        # Get known side effects for this medication
        medication_side_effects = self.side_effects[self.side_effects['medication_id'] == medication_id]
        
        # Prepare medication feature
        medication_feature = self.medication_encoder.transform([[medication_name]])
        
        # Adjust predictions based on patient data
        adjustment = 0
        if patient_data:
            age = patient_data.get('age', 0)
            if age > 65:
                adjustment = 0.1  # Increase severity for elderly
            elif age < 18:
                adjustment = 0.05  # Slight increase for minors
        
        # Prepare results
        side_effect_predictions = []
        
        for _, se in medication_side_effects.iterrows():
            severity = float(se['severity']) / 10.0  # Normalize to 0-1
            frequency = float(se['frequency'])
            
            # Adjust based on patient data
            severity += adjustment
            severity = min(1.0, max(0.0, severity))
            
            side_effect_predictions.append({
                'name': se['name'],
                'severity': severity,
                'frequency': frequency,
                'description': f"Possible side effect of {medication_name}"
            })
            
        # Sort by severity * frequency
        side_effect_predictions.sort(key=lambda x: x['severity'] * x['frequency'], reverse=True)
        
        return side_effect_predictions

def recommend_treatments(patient_data: Dict, patient_allergies: List[int] = None) -> Dict:
    """Recommend treatments and predict side effects
    
    Args:
        patient_data: Dictionary with patient information
        patient_allergies: List of allergy IDs
    
    Returns:
        Dictionary with recommendations and side effects
    """
    # Initialize recommender
    recommender = MedicationRecommender()
    
    # Get recommendations
    recommendations = recommender.recommend(patient_data, patient_allergies)
    
    # Initialize side effect predictor
    side_effect_predictor = SideEffectPredictor()
    
    # Get side effects for recommended medications
    for rec in recommendations['recommendations']:
        rec['side_effects'] = side_effect_predictor.predict_side_effects(
            rec['medication'], patient_data
        )
    
    return recommendations

if __name__ == "__main__":
    # Example usage
    patient_data = {
        'age': 65,
        'gender': 'Male',
        'diagnosis': 'Hypertension',
        'medications': ['Lisinopril']
    }
    
    patient_allergies = [7]  # Latex allergy
    
    recommendations = recommend_treatments(patient_data, patient_allergies)
    print(recommendations)
