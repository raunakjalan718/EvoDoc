import os
import pandas as pd
import numpy as np
from sklearn.preprocessing import OneHotEncoder, StandardScaler
import pickle

# Paths
DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "data")
PROCESSED_DIR = os.path.join(DATA_DIR, "processed")
MODEL_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "models")

class PatientFeatureExtractor:
    """Extract features from patient data for model input"""
    
    def __init__(self, load_from=None):
        """Initialize feature extractor
        
        Args:
            load_from: Path to load pre-trained extractors
        """
        if load_from:
            self.load(load_from)
        else:
            # Initialize encoders
            self.demographic_scaler = StandardScaler()
            self.diagnosis_encoder = OneHotEncoder(sparse_output=False, handle_unknown='ignore')
            self.medication_encoder = OneHotEncoder(sparse_output=False, handle_unknown='ignore')
            self.allergy_encoder = OneHotEncoder(sparse_output=False, handle_unknown='ignore')
    
    def fit(self, patients_df, diagnoses_df, medications_df, allergies_df):
        """Fit feature extractors to data
        
        Args:
            patients_df: DataFrame with patient information
            diagnoses_df: DataFrame with diagnoses information
            medications_df: DataFrame with medication information
            allergies_df: DataFrame with allergy information
        """
        # Fit demographic scaler
        demographic_features = patients_df[['age']].values
        self.demographic_scaler.fit(demographic_features)
        
        # Fit diagnosis encoder
        diagnosis_features = diagnoses_df[['diagnosis']].values
        self.diagnosis_encoder.fit(diagnosis_features)
        
        # Fit medication encoder
        medication_features = medications_df[['name']].values
        self.medication_encoder.fit(medication_features)
        
        # Fit allergy encoder
        allergy_features = allergies_df[['name']].values
        self.allergy_encoder.fit(allergy_features)
        
        return self
    
    def transform_patient(self, patient_data):
        """Transform patient data to feature vector
        
        Args:
            patient_data: Dictionary with patient information
        
        Returns:
            feature_vector: Numpy array with features
        """
        # Extract demographic features
        demographic = np.array([[patient_data.get('age', 0)]]) 
        demographic_scaled = self.demographic_scaler.transform(demographic)
        
        # Extract diagnosis features
        if 'diagnosis' in patient_data:
            diagnosis = np.array([[patient_data['diagnosis']]])
            diagnosis_encoded = self.diagnosis_encoder.transform(diagnosis)
        else:
            # Use empty array with correct shape if no diagnosis
            diagnosis_encoded = np.zeros((1, len(self.diagnosis_encoder.categories_[0])))
        
        # Extract medication features
        if 'medications' in patient_data and patient_data['medications']:
            # Handle multiple medications
            med_encoded_list = []
            for med in patient_data['medications']:
                med_array = np.array([[med]])
                med_encoded = self.medication_encoder.transform(med_array)
                med_encoded_list.append(med_encoded)
            # Combine multiple medications
            if med_encoded_list:
                medication_encoded = np.max(np.vstack(med_encoded_list), axis=0)
            else:
                medication_encoded = np.zeros((1, len(self.medication_encoder.categories_[0])))
        else:
            # Use empty array with correct shape if no medications
            medication_encoded = np.zeros((1, len(self.medication_encoder.categories_[0])))
        
        # Extract allergy features
        if 'allergies' in patient_data and patient_data['allergies']:
            # Handle multiple allergies
            allergy_encoded_list = []
            for allergy in patient_data['allergies']:
                allergy_array = np.array([[allergy]])
                allergy_encoded = self.allergy_encoder.transform(allergy_array)
                allergy_encoded_list.append(allergy_encoded)
            # Combine multiple allergies
            if allergy_encoded_list:
                allergy_encoded = np.max(np.vstack(allergy_encoded_list), axis=0)
            else:
                allergy_encoded = np.zeros((1, len(self.allergy_encoder.categories_[0])))
        else:
            # Use empty array with correct shape if no allergies
            allergy_encoded = np.zeros((1, len(self.allergy_encoder.categories_[0])))
        
        # Combine all features
        feature_vector = np.hstack([
            demographic_scaled,
            diagnosis_encoded,
            medication_encoded,
            allergy_encoded
        ])
        
        return feature_vector
    
    def save(self, save_path):
        """Save feature extractors to file
        
        Args:
            save_path: Path to save extractors
        """
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        
        with open(save_path, 'wb') as f:
            pickle.dump({
                'demographic_scaler': self.demographic_scaler,
                'diagnosis_encoder': self.diagnosis_encoder,
                'medication_encoder': self.medication_encoder,
                'allergy_encoder': self.allergy_encoder
            }, f)
    
    def load(self, load_path):
        """Load feature extractors from file
        
        Args:
            load_path: Path to load extractors from
        """
        with open(load_path, 'rb') as f:
            extractors = pickle.load(f)
            
            self.demographic_scaler = extractors['demographic_scaler']
            self.diagnosis_encoder = extractors['diagnosis_encoder']
            self.medication_encoder = extractors['medication_encoder']
            self.allergy_encoder = extractors['allergy_encoder']

def prepare_training_data(synthetic_dir, save_extractors=True):
    """Prepare training data from synthetic data
    
    Args:
        synthetic_dir: Directory with synthetic data
        save_extractors: Whether to save feature extractors
    
    Returns:
        X_train, y_train: Training data and targets
    """
    # Load synthetic data
    patients_df = pd.read_csv(os.path.join(synthetic_dir, "patients.csv"))
    medications_df = pd.read_csv(os.path.join(synthetic_dir, "medications.csv"))
    allergies_df = pd.read_csv(os.path.join(synthetic_dir, "allergies.csv"))
    appointments_df = pd.read_csv(os.path.join(synthetic_dir, "appointments.csv"))
    treatments_df = pd.read_csv(os.path.join(synthetic_dir, "treatments.csv"))
    feedbacks_df = pd.read_csv(os.path.join(synthetic_dir, "treatment_feedbacks.csv"))
    
    # Create diagnosis DataFrame from appointments
    diagnoses_df = appointments_df[['symptoms']].rename(columns={'symptoms': 'diagnosis'}).drop_duplicates()
    
    # Create feature extractor
    extractor = PatientFeatureExtractor()
    extractor.fit(patients_df, diagnoses_df, medications_df, allergies_df)
    
    # If save_extractors is True, save the feature extractor
    if save_extractors:
        os.makedirs(os.path.join(MODEL_DIR, "feature_extractors"), exist_ok=True)
        extractor.save(os.path.join(MODEL_DIR, "feature_extractors", "patient_feature_extractor.pkl"))
    
    # Prepare training data
    # Join treatments with feedback to get effectiveness data
    treatment_effectiveness = pd.merge(
        treatments_df,
        feedbacks_df[['treatment_id', 'effectiveness', 'side_effects']],
        left_on='id',
        right_on='treatment_id',
        how='inner',
        suffixes=('', '_feedback')  # Add explicit suffixes to avoid conflicts
    )
    
    # Join with appointments to get patient and diagnosis info
    treatment_data = pd.merge(
        treatment_effectiveness,
        appointments_df[['id', 'patient_id', 'symptoms']],
        left_on='appointment_id',
        right_on='id',
        how='inner',
        suffixes=('', '_appt')  # Add explicit suffixes to avoid conflicts
    )
    
    # Join with medications to get medication names
    treatment_data = pd.merge(
        treatment_data,
        medications_df[['id', 'name']],
        left_on='medication_id',
        right_on='id',
        how='inner',
        suffixes=('', '_med')  # Add explicit suffixes to avoid conflicts
    )
    
    # Join with patients to get patient demographics
    treatment_data = pd.merge(
        treatment_data,
        patients_df[['id', 'age', 'gender']],
        left_on='patient_id',
        right_on='id',
        how='inner',
        suffixes=('', '_pat')  # Add explicit suffixes to avoid conflicts
    )
    
    # Prepare feature vectors
    X_list = []
    y_list = []
    
    for _, row in treatment_data.iterrows():
        patient_data = {
            'age': row['age'],
            'gender': row['gender'],
            'diagnosis': row['symptoms'],
            'medications': [row['name']]
        }
        
        # Extract features
        X = extractor.transform_patient(patient_data)
        X_list.append(X)
        
        # Extract target (effectiveness)
        y = row['effectiveness'] / 10.0  # Normalize to 0-1 range
        y_list.append(y)
    
    # Combine all feature vectors
    X_train = np.vstack(X_list)
    y_train = np.array(y_list)
    
    return X_train, y_train

if __name__ == "__main__":
    # Example usage
    synthetic_dir = os.path.join(DATA_DIR, "synthetic")
    X_train, y_train = prepare_training_data(synthetic_dir)
    
    print(f"Training data shape: {X_train.shape}")
    print(f"Target data shape: {y_train.shape}")
