import os
import pandas as pd
import numpy as np
from sklearn.preprocessing import OneHotEncoder, StandardScaler
import pickle

# Paths
DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "data")
RAW_DIR = os.path.join(DATA_DIR, "raw")
PROCESSED_DIR = os.path.join(DATA_DIR, "processed")

def preprocess_drug_reviews():
    """Process Drug Review Dataset"""
    print("Processing Drug Review Dataset...")
    
    # Load train and test data
    train_path = os.path.join(RAW_DIR, "drugsComTrain_raw.tsv")
    test_path = os.path.join(RAW_DIR, "drugsComTest_raw.tsv")
    
    train_df = pd.read_csv(train_path, sep="\t")
    test_df = pd.read_csv(test_path, sep="\t")
    
    # Combine datasets for processing
    df = pd.concat([train_df, test_df])
    
    # Clean and transform data
    df = df.dropna(subset=['condition', 'review'])
    
    # Extract ratings and effectiveness info
    df['effectiveness'] = df['rating'].apply(lambda x: 1 if x >= 7 else 0 if x <= 4 else 0.5)
    
    # Process text reviews
    df['review_length'] = df['review'].apply(len)
    
    # Group by drug and condition to get average ratings
    drug_condition = df.groupby(['drugName', 'condition']).agg({
        'rating': 'mean',
        'effectiveness': 'mean',
        'usefulCount': 'sum',
        'review_length': 'mean',
    }).reset_index()
    
    # Create drug to condition mapping for recommendation
    drug_to_condition = {}
    for drug, group in df.groupby('drugName'):
        drug_to_condition[drug] = group['condition'].value_counts().to_dict()
    
    # Save processed data
    os.makedirs(PROCESSED_DIR, exist_ok=True)
    drug_condition.to_csv(os.path.join(PROCESSED_DIR, "drug_condition_ratings.csv"), index=False)
    
    with open(os.path.join(PROCESSED_DIR, "drug_condition_mapping.pkl"), 'wb') as f:
        pickle.dump(drug_to_condition, f)
    
    print("Drug Review Dataset processed successfully.")

def preprocess_faers_data():
    """Process FDA Adverse Event Reporting System data"""
    print("Processing FAERS data...")
    
    import json
    
    # Load FAERS sample data
    with open(os.path.join(RAW_DIR, "faers", "faers_sample.json"), 'r') as f:
        data = json.load(f)
    
    # Extract relevant information
    side_effects = []
    
    for result in data.get('results', []):
        patient_info = result.get('patient', {})
        reactions = patient_info.get('reaction', [])
        drugs = patient_info.get('drug', [])
        
        for drug in drugs:
            drug_name = drug.get('medicinalproduct', '')
            
            for reaction in reactions:
                side_effects.append({
                    'drug': drug_name,
                    'reaction': reaction.get('reactionmeddrapt', ''),
                    'serious': 1 if reaction.get('seriousness') else 0
                })
    
    # Convert to DataFrame
    side_effects_df = pd.DataFrame(side_effects)
    
    # Group by drug and reaction to get frequency
    grouped = side_effects_df.groupby(['drug', 'reaction']).agg({
        'serious': ['mean', 'sum', 'count']
    }).reset_index()
    
    grouped.columns = ['drug', 'reaction', 'severity', 'serious_count', 'frequency']
    
    # Calculate relative frequency
    total_counts = grouped.groupby('drug')['frequency'].sum().to_dict()
    grouped['relative_frequency'] = grouped.apply(
        lambda row: row['frequency'] / total_counts[row['drug']] if row['drug'] in total_counts else 0, 
        axis=1
    )
    
    # Save processed data
    grouped.to_csv(os.path.join(PROCESSED_DIR, "drug_side_effects.csv"), index=False)
    print("FAERS data processed successfully.")

def preprocess_mimic_data():
    """Process synthetic MIMIC-like data"""
    print("Processing synthetic MIMIC data...")
    
    # Load synthetic MIMIC data
    patients = pd.read_csv(os.path.join(RAW_DIR, "mimic", "patients.csv"))
    admissions = pd.read_csv(os.path.join(RAW_DIR, "mimic", "admissions.csv"))
    prescriptions = pd.read_csv(os.path.join(RAW_DIR, "mimic", "prescriptions.csv"))
    
    # Join data to create patient-treatment-outcome dataset
    patient_admissions = pd.merge(patients, admissions, on='subject_id')
    patient_treatments = pd.merge(patient_admissions, prescriptions, on='hadm_id')
    
    # Feature engineering
    # Calculate patient age at admission (simplified)
    patient_treatments['admission_year'] = pd.to_datetime(patient_treatments['admittime']).dt.year
    patient_treatments['birth_year'] = pd.to_datetime(patient_treatments['dob']).dt.year
    patient_treatments['age'] = patient_treatments['admission_year'] - patient_treatments['birth_year']
    
    # Calculate treatment duration
    patient_treatments['startdate'] = pd.to_datetime(patient_treatments['startdate'])
    patient_treatments['enddate'] = pd.to_datetime(patient_treatments['enddate'])
    patient_treatments['treatment_days'] = (patient_treatments['enddate'] - patient_treatments['startdate']).dt.days
    
    # Create treatment outcomes (synthetic)
    np.random.seed(42)
    patient_treatments['outcome_success'] = np.random.binomial(
        n=1, 
        p=0.7 + 0.1 * (patient_treatments['treatment_days'] / 10) - 0.1 * (patient_treatments['age'] / 100),
        size=len(patient_treatments)
    )
    
    # Select relevant columns
    treatment_data = patient_treatments[[
        'subject_id', 'gender', 'age', 'diagnosis', 'drug', 
        'dose_val_rx', 'dose_unit_rx', 'treatment_days', 'outcome_success'
    ]]
    
    # Save processed data
    treatment_data.to_csv(os.path.join(PROCESSED_DIR, "patient_treatments.csv"), index=False)
    print("Synthetic MIMIC data processed successfully.")

def create_model_ready_datasets():
    """Create final datasets ready for model training"""
    print("Creating model-ready datasets...")
    
    # Load processed data
    drug_condition = pd.read_csv(os.path.join(PROCESSED_DIR, "drug_condition_ratings.csv"))
    drug_side_effects = pd.read_csv(os.path.join(PROCESSED_DIR, "drug_side_effects.csv"))
    patient_treatments = pd.read_csv(os.path.join(PROCESSED_DIR, "patient_treatments.csv"))
    
    # 1. Treatment Recommendation Dataset
    # Combine drug effectiveness data with treatment outcomes
    drug_effectiveness = drug_condition[['drugName', 'condition', 'effectiveness', 'rating']]
    drug_effectiveness.columns = ['drug', 'diagnosis', 'effectiveness', 'rating']
    
    # Merge with patient treatments
    recommendation_data = pd.merge(
        patient_treatments, 
        drug_effectiveness,
        on=['drug', 'diagnosis'],
        how='left'
    )
    
    # Fill missing values
    recommendation_data['effectiveness'].fillna(recommendation_data['outcome_success'], inplace=True)
    recommendation_data['rating'].fillna(recommendation_data['effectiveness'] * 10, inplace=True)
    
    # 2. Side Effect Prediction Dataset
    # Merge side effect data with patient information
    side_effect_prediction = pd.merge(
        drug_side_effects,
        patient_treatments[['subject_id', 'gender', 'age', 'drug']],
        on='drug',
        how='left'
    )
    
    # Create feature matrices and target variables
    # For recommendation model
    X_rec = recommendation_data[['age', 'diagnosis', 'drug', 'treatment_days']]
    y_rec = recommendation_data['effectiveness']
    
    # One-hot encode categorical features
    encoder = OneHotEncoder(sparse_output=False, handle_unknown='ignore')
    X_rec_cat = encoder.fit_transform(X_rec[['diagnosis', 'drug']])
    
    # Combine with numerical features
    X_rec_num = X_rec[['age', 'treatment_days']].values
    X_rec_final = np.hstack([X_rec_num, X_rec_cat])
    
    # For side effect model
    X_se = side_effect_prediction[['drug', 'reaction', 'age', 'gender']]
    y_se = side_effect_prediction[['severity', 'relative_frequency']]
    
    # One-hot encode categorical features
    encoder_se = OneHotEncoder(sparse_output=False, handle_unknown='ignore')
    X_se_cat = encoder_se.fit_transform(X_se[['drug', 'reaction', 'gender']])
    
    # Combine with numerical features
    X_se_num = X_se[['age']].values
    X_se_final = np.hstack([X_se_num, X_se_cat])
    
    # Save model-ready datasets
    model_dir = os.path.join(PROCESSED_DIR, "model_ready")
    os.makedirs(model_dir, exist_ok=True)
    
    # Save training data
    np.save(os.path.join(model_dir, "X_recommendation.npy"), X_rec_final)
    np.save(os.path.join(model_dir, "y_recommendation.npy"), y_rec.values)
    np.save(os.path.join(model_dir, "X_side_effect.npy"), X_se_final)
    np.save(os.path.join(model_dir, "y_side_effect.npy"), y_se.values)
    
    # Save encoders for prediction
    with open(os.path.join(model_dir, "recommendation_encoder.pkl"), 'wb') as f:
        pickle.dump(encoder, f)
    
    with open(os.path.join(model_dir, "side_effect_encoder.pkl"), 'wb') as f:
        pickle.dump(encoder_se, f)
    
    # Save feature names for reference
    feature_names = {
        'recommendation': {
            'numerical': ['age', 'treatment_days'],
            'categorical': ['diagnosis', 'drug'],
            'categorical_values': {
                'diagnosis': list(X_rec['diagnosis'].unique()),
                'drug': list(X_rec['drug'].unique())
            }
        },
        'side_effect': {
            'numerical': ['age'],
            'categorical': ['drug', 'reaction', 'gender'],
            'categorical_values': {
                'drug': list(X_se['drug'].unique()),
                'reaction': list(X_se['reaction'].unique()),
                'gender': list(X_se['gender'].unique())
            }
        }
    }
    
    with open(os.path.join(model_dir, "feature_names.pkl"), 'wb') as f:
        pickle.dump(feature_names, f)
    
    print("Model-ready datasets created successfully.")

def main():
    # Create processed directory if it doesn't exist
    os.makedirs(PROCESSED_DIR, exist_ok=True)
    
    # Process datasets
    preprocess_drug_reviews()
    preprocess_faers_data()
    preprocess_mimic_data()
    
    # Create model-ready datasets
    create_model_ready_datasets()
    
    print("All data preprocessing completed successfully!")

if __name__ == "__main__":
    main()
