import os
import pickle
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import mean_squared_error, r2_score
import xgboost as xgb
from pathlib import Path
import time
import sys

# Constants
DATA_DIR = Path("./data")
MODELS_DIR = Path("./models")
MODELS_DIR.mkdir(exist_ok=True)

def train_models(force=False):
    """Train treatment recommendation and side effect prediction models"""
    print("===== EvoDoc Model Trainer =====")
    
    # Check if models are already trained
    if os.path.exists(MODELS_DIR / "training_complete.flag") and not force:
        print("Models already trained. Use --force to re-train.")
        return
        
    # Check if datasets exist
    if not os.path.exists(DATA_DIR / "download_complete.flag"):
        print("Datasets not found. Please run download_data.py first.")
        return
    
    print("Loading datasets and training models...")
    
    # Load treatment data
    try:
        treatment_data = pd.read_csv(DATA_DIR / "treatment_data.csv")
        print(f"Loaded {len(treatment_data)} treatment records.")
        
        # Quick data validation
        required_columns = ['subject_id', 'diagnosis', 'medication', 'effectiveness', 'age', 'gender']
        missing_columns = [col for col in required_columns if col not in treatment_data.columns]
        if missing_columns:
            print(f"Warning: Treatment data missing columns: {', '.join(missing_columns)}")
        
        # Show dataset summary
        print(f"Dataset summary:")
        print(f" - Patient count: {treatment_data['subject_id'].nunique()}")
        print(f" - Diagnosis count: {treatment_data['diagnosis'].nunique()}")
        print(f" - Medication count: {treatment_data['medication'].nunique()}")
        print(f" - Effectiveness range: {treatment_data['effectiveness'].min()} - {treatment_data['effectiveness'].max()}")
        
        # Check effectiveness distribution
        effectiveness_bins = pd.cut(treatment_data['effectiveness'], bins=10)
        print("\nEffectiveness distribution:")
        print(effectiveness_bins.value_counts().sort_index())
        
    except Exception as e:
        print(f"Error loading treatment data: {e}")
        return
    
    # Load side effect data
    try:
        side_effects = pd.read_csv(DATA_DIR / "side_effects.csv")
        print(f"Loaded {len(side_effects)} side effect records.")
    except Exception as e:
        print(f"Error loading side effect data: {e}")
        return
    
    # Enhance the training data with additional features
    print("\nEnhancing data with medical domain features...")
    enhanced_data = enhance_training_data(treatment_data)
    
    # Create train-test split
    train_data, test_data = train_test_split(enhanced_data, test_size=0.2, random_state=42)
    
    # Train recommendation model
    print("\nTraining improved treatment recommendation model...")
    start_time = time.time()
    recommendation_model, encoders = train_recommendation_model(train_data)
    training_time = time.time() - start_time
    print(f"Recommendation model training completed in {training_time:.2f} seconds.")
    
    # Evaluate the model on test data
    print("\nEvaluating on test data...")
    evaluate_model(recommendation_model, encoders, test_data)
    
    # Train side effect models
    print("\nTraining side effect prediction models...")
    start_time = time.time()
    side_effect_models = train_side_effect_models(side_effects)
    training_time = time.time() - start_time
    print(f"Side effect models training completed in {training_time:.2f} seconds.")
    
    # Combine all models
    models = {
        "recommendation": recommendation_model,
        "side_effect_frequency": side_effect_models["frequency"],
        "side_effect_severity": side_effect_models["severity"],
        "side_effect_encoder": side_effect_models["medication_encoder"]
    }
    
    # Save models and encoders
    try:
        with open(MODELS_DIR / "models.pkl", "wb") as f:
            pickle.dump(models, f)
            
        with open(MODELS_DIR / "encoders.pkl", "wb") as f:
            pickle.dump(encoders, f)
            
        print("\nModels and encoders saved successfully.")
    except Exception as e:
        print(f"Error saving models: {e}")
        return
    
    # Create flag file to indicate training is complete
    with open(MODELS_DIR / "training_complete.flag", "w") as f:
        f.write("Training completed on " + pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S"))
    
    print("\nModel training complete! You can now run evaluate_models.py or recommend.py")

def enhance_training_data(data):
    """Add domain-specific medical features to improve model performance"""
    print("Adding medical domain knowledge features...")
    enhanced_data = data.copy()
    
    # 1. Load first-line treatment data if available
    first_line_file = DATA_DIR / "first_line_treatments.csv"
    if first_line_file.exists():
        first_line_df = pd.read_csv(first_line_file)
        
        # Create first-line indicator
        first_line_map = {}
        for _, row in first_line_df.iterrows():
            condition = row['condition']
            medication = row['medication']
            if condition not in first_line_map:
                first_line_map[condition] = []
            first_line_map[condition].append(medication)
        
        # Add first-line indicator
        def is_first_line(row):
            if row['diagnosis'] in first_line_map:
                return 1 if row['medication'] in first_line_map[row['diagnosis']] else 0
            return 0
            
        enhanced_data['is_first_line'] = enhanced_data.apply(is_first_line, axis=1)
    else:
        # Fallback to use the high effectiveness treatments as first-line
        print("First-line treatment data not found, using effectiveness as proxy.")
        high_effectiveness = enhanced_data[enhanced_data['effectiveness'] >= 8]
        first_line_map = {}
        for _, row in high_effectiveness.iterrows():
            diag = row['diagnosis']
            med = row['medication']
            if diag not in first_line_map:
                first_line_map[diag] = set()
            first_line_map[diag].add(med)
            
        enhanced_data['is_first_line'] = enhanced_data.apply(
            lambda row: 1 if row['medication'] in first_line_map.get(row['diagnosis'], set()) else 0,
            axis=1
        )
    
    # 2. Add age-condition interaction features
    # Create age groups
    if 'age_group' not in enhanced_data.columns:
        enhanced_data['age_group'] = pd.cut(
            enhanced_data['age'], 
            bins=[0, 18, 40, 65, 100], 
            labels=['pediatric', 'young_adult', 'middle_age', 'elderly']
        )
    
    # 3. Add medication class features
    med_class_file = DATA_DIR / "drugbank_sample.json"
    if med_class_file.exists():
        import json
        with open(med_class_file, 'r') as f:
            drug_data = json.load(f)
            
        med_class_map = {}
        for drug in drug_data.get('drugs', []):
            if 'name' in drug and 'drug_class' in drug:
                med_class_map[drug['name']] = drug['drug_class']
                
        enhanced_data['med_class'] = enhanced_data['medication'].map(med_class_map)
        
        # Fill missing values
        if enhanced_data['med_class'].isna().sum() > 0:
            print(f"Warning: {enhanced_data['med_class'].isna().sum()} medications without class information")
            enhanced_data['med_class'] = enhanced_data['med_class'].fillna('Unknown')
    else:
        print("Drug class data not found, skipping medication class features.")
    
    # 4. Add condition group features
    condition_groups = {
        "respiratory": ["Pneumonia", "Bronchitis", "Asthma", "COPD", "Allergic Rhinitis"],
        "cardiovascular": ["Hypertension", "Heart failure"],
        "metabolic": ["Type 2 Diabetes", "Obesity"],
        "mental_health": ["Depression", "Anxiety"],
        "pain": ["Migraine", "Osteoarthritis", "Pain"],
        "infection": ["Pneumonia", "Urinary Tract Infection", "Bronchitis"]
    }
    
    for group, conditions in condition_groups.items():
        enhanced_data[f'group_{group}'] = enhanced_data['diagnosis'].apply(
            lambda x: 1 if x in conditions else 0)
    
    print(f"Added {len(enhanced_data.columns) - len(data.columns)} new features")
    return enhanced_data

def train_recommendation_model(treatment_data):
    """Train an improved treatment recommendation model"""
    print("Preparing data for recommendation model training...")
    
    # Create encoders for categorical variables
    print("Creating and fitting feature encoders...")
    diagnosis_encoder = OneHotEncoder(sparse_output=False, handle_unknown='ignore')
    medication_encoder = OneHotEncoder(sparse_output=False, handle_unknown='ignore')
    gender_encoder = OneHotEncoder(sparse_output=False, handle_unknown='ignore')
    
    # Add encoders for new categorical features
    encoders = {}
    categorical_features = ['diagnosis', 'medication', 'gender']
    
    if 'med_class' in treatment_data.columns:
        categorical_features.append('med_class')
        encoders['med_class'] = OneHotEncoder(sparse_output=False, handle_unknown='ignore')
    
    if 'age_group' in treatment_data.columns:
        categorical_features.append('age_group')
        encoders['age_group'] = OneHotEncoder(sparse_output=False, handle_unknown='ignore')
    
    # Fit encoders
    diagnosis_encoder.fit(treatment_data[['diagnosis']])
    medication_encoder.fit(treatment_data[['medication']])
    gender_encoder.fit(treatment_data[['gender']])
    
    for feature in ['med_class', 'age_group']:
        if feature in treatment_data.columns:
            encoders[feature].fit(treatment_data[[feature]])
    
    # Prepare numerical features
    numerical_features = ['age']
    if 'is_first_line' in treatment_data.columns:
        numerical_features.append('is_first_line')
    
    # Add condition group features
    group_features = [col for col in treatment_data.columns if col.startswith('group_')]
    numerical_features.extend(group_features)
    
    # Scale numerical features
    print("Scaling numerical features...")
    age_scaler = StandardScaler()
    numerical_data = treatment_data[numerical_features].copy()
    
    # Replace NaNs with 0
    numerical_data = numerical_data.fillna(0)
    
    X_numerical = age_scaler.fit_transform(numerical_data)
    
    # Transform categorical features
    print("Transforming categorical features...")
    X_diagnosis = diagnosis_encoder.transform(treatment_data[['diagnosis']])
    X_medication = medication_encoder.transform(treatment_data[['medication']])
    X_gender = gender_encoder.transform(treatment_data[['gender']])
    
    # Build feature matrix
    feature_parts = [X_numerical, X_gender, X_diagnosis, X_medication]
    
    # Add optional encoded features
    for feature in ['med_class', 'age_group']:
        if feature in treatment_data.columns:
            X_feature = encoders[feature].transform(treatment_data[[feature]])
            feature_parts.append(X_feature)
    
    # Combine all features
    X = np.hstack(feature_parts)
    
    print(f"Combined feature matrix shape: {X.shape}")
    
    # Target: effectiveness (normalize to 0-1 range)
    y = treatment_data['effectiveness'].values / 10.0
    
    # Try multiple model types
    models = {
        'gradient_boosting': GradientBoostingRegressor(
            n_estimators=200, 
            learning_rate=0.05, 
            max_depth=4,
            min_samples_split=5,
            min_samples_leaf=10,
            subsample=0.8,
            random_state=42
        ),
        'random_forest': RandomForestRegressor(
            n_estimators=200, 
            max_features='sqrt', 
            min_samples_leaf=5, 
            random_state=42
        ),
        'xgboost': xgb.XGBRegressor(
            n_estimators=200, 
            learning_rate=0.05, 
            max_depth=4, 
            gamma=0.1,
            reg_alpha=0.1,
            reg_lambda=1.0,
            random_state=42
        )
    }
    
    # Find best model using cross-validation
    print("Comparing models using cross-validation...")
    best_model_name = None
    best_score = float('-inf')
    cv_results = {}
    
    for name, model in models.items():
        cv_scores = cross_val_score(model, X, y, cv=5, scoring='r2')
        mean_score = cv_scores.mean()
        cv_results[name] = {
            'mean_r2': mean_score,
            'std_r2': cv_scores.std()
        }
        print(f"{name}: Mean R² = {mean_score:.4f}, Std = {cv_results[name]['std_r2']:.4f}")
        
        if mean_score > best_score:
            best_score = mean_score
            best_model_name = name
    
    # Train best model on full dataset
    print(f"\nTraining best model ({best_model_name}) on full dataset...")
    best_model = models[best_model_name]
    best_model.fit(X, y)
    
    # Store encoders
    encoders_dict = {
        "diagnosis": diagnosis_encoder,
        "medication": medication_encoder,
        "gender": gender_encoder,
        "age": age_scaler
    }
    
    # Add optional encoders
    for feature in ['med_class', 'age_group']:
        if feature in encoders:
            encoders_dict[feature] = encoders[feature]
    
    # Save feature names for importance analysis
    feature_names = []
    feature_names.extend([f'numerical_{i}' for i, name in enumerate(numerical_features)])
    feature_names.extend([f'gender_{cat}' for cat in gender_encoder.categories_[0]])
    feature_names.extend([f'diagnosis_{cat}' for cat in diagnosis_encoder.categories_[0]])
    feature_names.extend([f'medication_{cat}' for cat in medication_encoder.categories_[0]])
    
    for feature in ['med_class', 'age_group']:
        if feature in encoders:
            feature_names.extend([f'{feature}_{cat}' for cat in encoders[feature].categories_[0]])
    
    encoders_dict['feature_names'] = feature_names
    
    return best_model, encoders_dict

def evaluate_model(model, encoders, test_data):
    """Evaluate model performance on test data"""
    # Extract features from test data
    numerical_features = ['age']
    if 'is_first_line' in test_data.columns:
        numerical_features.append('is_first_line')
    
    # Add condition group features
    group_features = [col for col in test_data.columns if col.startswith('group_')]
    numerical_features.extend(group_features)
    
    # Prepare numerical data
    numerical_data = test_data[numerical_features].copy()
    numerical_data = numerical_data.fillna(0)
    X_numerical = encoders['age'].transform(numerical_data)
    
    # Transform categorical features
    X_gender = encoders['gender'].transform(test_data[['gender']])
    X_diagnosis = encoders['diagnosis'].transform(test_data[['diagnosis']])
    X_medication = encoders['medication'].transform(test_data[['medication']])
    
    # Build feature matrix
    feature_parts = [X_numerical, X_gender, X_diagnosis, X_medication]
    
    # Add optional encoded features
    for feature in ['med_class', 'age_group']:
        if feature in encoders and feature in test_data.columns:
            X_feature = encoders[feature].transform(test_data[[feature]])
            feature_parts.append(X_feature)
    
    # Combine all features
    X = np.hstack(feature_parts)
    
    # Target
    y_true = test_data['effectiveness'].values / 10.0
    
    # Make predictions
    y_pred = model.predict(X)
    
    # Calculate metrics
    mse = mean_squared_error(y_true, y_pred)
    rmse = np.sqrt(mse)
    r2 = r2_score(y_true, y_pred)
    
    # Calculate binary classification metrics (effective vs not)
    threshold = 0.7  # 7/10 effectiveness
    y_true_binary = (y_true >= threshold).astype(int)
    y_pred_binary = (y_pred >= threshold).astype(int)
    
    accuracy = (y_true_binary == y_pred_binary).mean()
    
    print(f"Test set evaluation:")
    print(f"  MSE:      {mse:.4f}")
    print(f"  RMSE:     {rmse:.4f}")
    print(f"  R²:       {r2:.4f}")
    print(f"  Accuracy: {accuracy:.4f}")
    
    # Analyze feature importances if available
    if hasattr(model, 'feature_importances_'):
        importances = model.feature_importances_
        feature_names = encoders.get('feature_names', [f"Feature {i}" for i in range(len(importances))])
        
        # Ensure lengths match
        feature_names = feature_names[:len(importances)]
        
        # Get top 10 features
        indices = np.argsort(importances)[-10:]
        print("\nTop 10 important features:")
        for i in reversed(indices):
            print(f"  {feature_names[i]}: {importances[i]:.4f}")
    
    return {
        'mse': mse,
        'rmse': rmse,
        'r2': r2,
        'accuracy': accuracy
    }

def train_side_effect_models(side_effects):
    """Train models for side effect prediction"""
    print(f"Training side effect models with {len(side_effects)} records...")
    
    # Create medication encoder
    medication_encoder = OneHotEncoder(sparse_output=False, handle_unknown='ignore')
    medication_encoder.fit(side_effects[['medication']])
    
    print(f"Side effect medications: {len(medication_encoder.categories_[0])}")
    
    # Transform data
    X = medication_encoder.transform(side_effects[['medication']])
    
    # Train frequency model
    print("Training frequency prediction model...")
    y_freq = side_effects['frequency'].values
    freq_model = RandomForestRegressor(
        n_estimators=100,
        max_depth=5,
        min_samples_leaf=3,
        random_state=42
    )
    freq_model.fit(X, y_freq)
    
    # Train severity model
    print("Training severity prediction model...")
    y_sev = side_effects['severity'].values / 10.0  # Normalize to 0-1
    sev_model = RandomForestRegressor(
        n_estimators=100,
        max_depth=5,
        min_samples_leaf=3,
        random_state=42
    )
    sev_model.fit(X, y_sev)
    
    return {
        "frequency": freq_model,
        "severity": sev_model,
        "medication_encoder": medication_encoder
    }

if __name__ == "__main__":
    # Check if --force flag is provided
    force = "--force" in sys.argv
    train_models(force)
