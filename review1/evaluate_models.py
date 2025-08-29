import os
import pickle
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import mean_squared_error, r2_score, precision_score, recall_score
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from pathlib import Path

# Constants
DATA_DIR = Path("./data")
MODELS_DIR = Path("./models")
EVAL_DIR = Path("./evaluation")
EVAL_DIR.mkdir(exist_ok=True)

def evaluate_models():
    """Evaluate model performance using cross-validation and test data"""
    print("===== EvoDoc Model Evaluation =====")
    
    # Check if data exists
    if not os.path.exists(DATA_DIR / "download_complete.flag"):
        print("Datasets not found. Please run download_data.py first.")
        return
    
    # Load existing models if available
    models_exist = os.path.exists(MODELS_DIR / "models.pkl")
    
    if models_exist:
        print("Loading existing models for evaluation...")
        with open(MODELS_DIR / "models.pkl", "rb") as f:
            models = pickle.load(f)
        with open(MODELS_DIR / "encoders.pkl", "rb") as f:
            encoders = pickle.load(f)
    else:
        print("No pre-trained models found. Please run train_models.py first.")
        return
    
    # Create evaluation dataset
    print("Generating evaluation datasets...")
    treatment_data, treatment_test = generate_evaluation_data()
    
    # Evaluate recommendation model
    print("\nEvaluating treatment recommendation model...")
    evaluate_recommendation_model(models, encoders, treatment_data, treatment_test)
    
    # Evaluate on specific clinical scenarios
    print("\nEvaluating on specific clinical scenarios...")
    evaluate_clinical_scenarios(models, encoders)
    
    print("\nEvaluation complete! Results saved to the 'evaluation' directory.")

def generate_evaluation_data():
    """Generate a more comprehensive evaluation dataset"""
    print("Loading base training data...")
    
    # Load existing treatment data
    base_treatment_data = pd.read_csv(DATA_DIR / "treatment_data.csv")
    
    # Create a larger, more diverse test set
    print("Generating synthetic test data with diverse patient profiles...")
    
    # Generate synthetic patients with diverse demographics
    np.random.seed(100)  # Different seed than training data
    n_patients = 200  # Double the size
    
    patient_ids = np.arange(1000, 1000 + n_patients)  # Different range than training data
    
    # More diverse age distribution
    ages = np.concatenate([
        np.random.normal(30, 10, size=n_patients//4),  # Young adults
        np.random.normal(50, 10, size=n_patients//4),  # Middle-aged
        np.random.normal(70, 10, size=n_patients//4),  # Elderly
        np.random.uniform(18, 90, size=n_patients//4)   # Uniform spread
    ])
    ages = np.clip(ages, 18, 95).astype(int)
    
    # More balanced gender distribution
    genders = np.random.choice(['M', 'F'], size=n_patients, p=[0.5, 0.5])
    
    patients = pd.DataFrame({
        'subject_id': patient_ids,
        'gender': genders,
        'age': ages
    })
    
    # Get all unique diagnoses and medications from the base dataset
    all_diagnoses = base_treatment_data['diagnosis'].unique()
    all_medications = base_treatment_data['medication'].unique()
    
    # Calculate medication effectiveness for each diagnosis from the base data
    diag_med_effectiveness = {}
    for diagnosis in all_diagnoses:
        diag_data = base_treatment_data[base_treatment_data['diagnosis'] == diagnosis]
        diag_med_effectiveness[diagnosis] = {}
        
        for medication in all_medications:
            med_data = diag_data[diag_data['medication'] == medication]
            if len(med_data) > 0:
                diag_med_effectiveness[diagnosis][medication] = med_data['effectiveness'].mean()
            else:
                # If no data for this combination, use a low effectiveness
                diag_med_effectiveness[diagnosis][medication] = 3.0
    
    # Generate synthetic treatments for evaluation
    treatments = []
    
    # Assign diagnoses to patients
    for patient_id in patient_ids:
        n_diagnoses = np.random.randint(1, 4)
        diagnoses = np.random.choice(all_diagnoses, size=n_diagnoses, replace=False)
        
        for diagnosis in diagnoses:
            # Get the effectiveness dict for this diagnosis
            med_effectiveness = diag_med_effectiveness.get(diagnosis, {})
            
            # Sort medications by their effectiveness for this diagnosis
            sorted_meds = sorted(med_effectiveness.items(), key=lambda x: x[1], reverse=True)
            
            # Select some effective and some ineffective treatments
            if len(sorted_meds) > 0:
                # Top medications
                for medication, base_eff in sorted_meds[:2]:  # 2 most effective
                    # Add some noise to effectiveness
                    effectiveness = min(10, max(1, int(round(
                        base_eff + np.random.normal(0, 1)
                    ))))
                    
                    treatments.append({
                        'subject_id': patient_id,
                        'diagnosis': diagnosis,
                        'medication': medication,
                        'effectiveness': effectiveness
                    })
                
                # Bottom medications
                if len(sorted_meds) > 3:
                    for medication, base_eff in sorted_meds[-2:]:  # 2 least effective
                        # Add some noise to effectiveness
                        effectiveness = min(10, max(1, int(round(
                            base_eff + np.random.normal(0, 1)
                        ))))
                        
                        treatments.append({
                            'subject_id': patient_id,
                            'diagnosis': diagnosis,
                            'medication': medication,
                            'effectiveness': effectiveness
                        })
    
    treatments_df = pd.DataFrame(treatments)
    
    # Create final evaluation dataset
    test_data = pd.merge(
        treatments_df,
        patients,
        on="subject_id"
    )
    
    # Save evaluation data
    test_data.to_csv(DATA_DIR / "evaluation_data.csv", index=False)
    
    return base_treatment_data, test_data

def prepare_features(data, encoders):
    """Prepare features for model evaluation"""
    # Prepare numerical features
    numerical_features = ['age']
    if 'is_first_line' in data.columns:
        numerical_features.append('is_first_line')
    
    # Add group features if they exist
    group_features = [col for col in data.columns if col.startswith('group_')]
    numerical_features.extend(group_features)
    
    # Fill missing numerical values with 0
    numerical_data = data[numerical_features].copy().fillna(0)
    
    try:
        X_numerical = encoders['age'].transform(numerical_data)
    except:
        # If there's an error with the full matrix, try just using age
        X_numerical = encoders['age'].transform(data[['age']])
    
    # Transform categorical features
    X_gender = encoders['gender'].transform(data[['gender']])
    
    try:
        X_diagnosis = encoders['diagnosis'].transform(data[['diagnosis']])
    except:
        # Handle unknown diagnoses
        diagnosis_categories = encoders['diagnosis'].categories_[0]
        X_diagnosis = np.zeros((len(data), len(diagnosis_categories)))
    
    try:
        X_medication = encoders['medication'].transform(data[['medication']])
    except:
        # Handle unknown medications
        medication_categories = encoders['medication'].categories_[0]
        X_medication = np.zeros((len(data), len(medication_categories)))
    
    # Start with basic features
    feature_parts = [X_numerical, X_gender, X_diagnosis, X_medication]
    
    # Add optional features if available
    for feature in ['med_class', 'age_group']:
        if feature in encoders and feature in data.columns:
            try:
                X_feature = encoders[feature].transform(data[[feature]])
                feature_parts.append(X_feature)
            except:
                # Skip if there's an issue with this feature
                pass
    
    # Combine all features
    X = np.hstack(feature_parts)
    return X

def evaluate_recommendation_model(models, encoders, training_data, test_data):
    """Evaluate the treatment recommendation model"""
    recommendation_model = models["recommendation"]
    
    # Prepare features for test data
    X_test = prepare_features(test_data, encoders)
    
    # Normalize effectiveness
    y_test = test_data['effectiveness'].values / 10.0
    
    # Make predictions
    y_pred = recommendation_model.predict(X_test)
    
    # Calculate metrics
    mse = mean_squared_error(y_test, y_pred)
    rmse = np.sqrt(mse)
    r2 = r2_score(y_test, y_pred)
    
    # Calculate binary accuracy (effective vs not effective) using threshold of 0.7
    y_test_binary = (y_test >= 0.7).astype(int)
    y_pred_binary = (y_pred >= 0.7).astype(int)
    precision = precision_score(y_test_binary, y_pred_binary)
    recall = recall_score(y_test_binary, y_pred_binary)
    
    # Print metrics
    print(f"Mean Squared Error: {mse:.4f}")
    print(f"Root Mean Squared Error: {rmse:.4f}")
    print(f"R² Score: {r2:.4f}")
    print(f"Precision (effective treatments): {precision:.4f}")
    print(f"Recall (effective treatments): {recall:.4f}")
    
    # Cross-validation on training data
    print("\nPerforming cross-validation on training data...")
    X_train = prepare_features(training_data, encoders)
    y_train = training_data['effectiveness'].values / 10.0
    
    cv_scores = cross_val_score(
        recommendation_model, 
        X_train, 
        y_train, 
        cv=5, 
        scoring='neg_mean_squared_error'
    )
    
    cv_rmse = np.sqrt(-cv_scores)
    print(f"Cross-validation RMSE: {cv_rmse.mean():.4f} (±{cv_rmse.std():.4f})")
    
    # Generate visualizations
    # 1. Predicted vs Actual Effectiveness
    plt.figure(figsize=(10, 6))
    plt.scatter(y_test, y_pred, alpha=0.3)
    plt.plot([0, 1], [0, 1], 'r--')
    plt.xlabel('Actual Effectiveness')
    plt.ylabel('Predicted Effectiveness')
    plt.title('Predicted vs Actual Treatment Effectiveness')
    plt.tight_layout()
    plt.savefig(EVAL_DIR / "pred_vs_actual.png")
    
    # 2. Prediction Error Distribution
    plt.figure(figsize=(10, 6))
    errors = y_pred - y_test
    sns.histplot(errors, kde=True)
    plt.xlabel('Prediction Error')
    plt.ylabel('Frequency')
    plt.title('Distribution of Prediction Errors')
    plt.tight_layout()
    plt.savefig(EVAL_DIR / "error_distribution.png")
    
    # 3. Effectiveness by Medication (top 10)
    plt.figure(figsize=(12, 8))
    medication_effectiveness = test_data.groupby('medication')['effectiveness'].mean().sort_values(ascending=False).head(10)
    sns.barplot(x=medication_effectiveness.values, y=medication_effectiveness.index)
    plt.xlabel('Average Effectiveness')
    plt.title('Top 10 Most Effective Medications')
    plt.tight_layout()
    plt.savefig(EVAL_DIR / "top_medications.png")
    
    # Save evaluation metrics
    metrics = {
        "mse": mse,
        "rmse": rmse,
        "r2": r2,
        "precision": precision,
        "recall": recall,
        "cv_rmse_mean": cv_rmse.mean(),
        "cv_rmse_std": cv_rmse.std()
    }
    
    pd.DataFrame([metrics]).to_csv(EVAL_DIR / "metrics.csv", index=False)

def evaluate_clinical_scenarios(models, encoders):
    """Evaluate model on specific clinical scenarios"""
    model = models["recommendation"]
    
    # Define some clinical scenarios
    scenarios = [
        {
            "name": "Elderly Patient with Hypertension",
            "age": 78,
            "gender": "F",
            "diagnosis": "Hypertension",
            "expected_medications": ["Lisinopril", "Amlodipine", "Hydrochlorothiazide"]
        },
        {
            "name": "Young Adult with Respiratory Infection",
            "age": 22,
            "gender": "M",
            "diagnosis": "Bronchitis",
            "expected_medications": ["Azithromycin", "Amoxicillin", "Doxycycline"]
        },
        {
            "name": "Middle-aged Patient with Diabetes",
            "age": 52,
            "gender": "M",
            "diagnosis": "Type 2 Diabetes",
            "expected_medications": ["Metformin", "Glipizide", "Sitagliptin"]
        },
        {
            "name": "Child with Allergies",
            "age": 12,
            "gender": "F",
            "diagnosis": "Allergic Rhinitis",
            "expected_medications": ["Cetirizine", "Loratadine", "Fluticasone"]
        },
        {
            "name": "Adult with Mental Health Issues",
            "age": 35,
            "gender": "F",
            "diagnosis": "Anxiety",
            "expected_medications": ["Sertraline", "Citalopram", "Escitalopram"]
        }
    ]
    
    # Available medications for prediction
    try:
        available_medications = list(encoders["medication"].categories_[0])
    except:
        print("Warning: Could not get medication list from encoder.")
        available_medications = ["Amoxicillin", "Azithromycin", "Lisinopril", "Metformin", "Ibuprofen", "Loratadine"]
    
    # Evaluate each scenario
    scenario_results = []
    
    for scenario in scenarios:
        # Prepare features
        # Age
        age_scaled = encoders["age"].transform([[scenario["age"]]])
        
        # Gender
        try:
            gender_encoded = encoders["gender"].transform([[scenario["gender"]]])
        except:
            gender_encoded = np.array([[1, 0]]) if scenario["gender"] == "M" else np.array([[0, 1]])
        
        # Diagnosis
        try:
            diagnosis_encoded = encoders["diagnosis"].transform([[scenario["diagnosis"]]])
        except:
            # If diagnosis not in encoder, use zeros
            diagnosis_encoded = np.zeros((1, len(encoders["diagnosis"].categories_[0])))
        
        # Evaluate each medication
        predictions = []
        
        for medication in available_medications:
            # Create medication feature
            med_feature = np.zeros((1, len(available_medications)))
            try:
                med_idx = np.where(available_medications == medication)[0][0]
                med_feature[0, med_idx] = 1
            except:
                continue
            
            # Combine features
            X = np.hstack([
                age_scaled,
                gender_encoded,
                diagnosis_encoded,
                med_feature
            ])
            
            # Predict effectiveness
            try:
                effectiveness = float(model.predict(X)[0])
                predictions.append((medication, effectiveness))
            except:
                continue
        
        # Sort by effectiveness
        predictions.sort(key=lambda x: x[1], reverse=True)
        
        # Get top 3 medications
        top_medications = [p[0] for p in predictions[:3]]
        
        # Check if top predictions include expected medications
        match_count = sum(1 for med in scenario["expected_medications"] if med in top_medications)
        match_percentage = match_count / len(scenario["expected_medications"]) if scenario["expected_medications"] else 0
        
        scenario_results.append({
            "scenario": scenario["name"],
            "top_predictions": top_medications,
            "expected_medications": scenario["expected_medications"],
            "match_percentage": match_percentage
        })
    
    # Save results
    pd.DataFrame(scenario_results).to_csv(EVAL_DIR / "scenario_evaluation.csv", index=False)
    
    # Print results
    for result in scenario_results:
        print(f"\nScenario: {result['scenario']}")
        print(f"Top Recommendations: {', '.join(result['top_predictions'])}")
        print(f"Expected Medications: {', '.join(result['expected_medications'])}")
        print(f"Match Percentage: {result['match_percentage']:.0%}")

if __name__ == "__main__":
    evaluate_models()
    print("\nNow run recommend.py to use the model for treatment recommendations")
