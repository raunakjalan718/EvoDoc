import os
import numpy as np
import pandas as pd
import pickle
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.linear_model import LinearRegression
import xgboost as xgb
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
import matplotlib.pyplot as plt
from .features import prepare_training_data

# Paths
DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "data")
MODEL_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "models")
SYNTHETIC_DIR = os.path.join(DATA_DIR, "synthetic")
TRAINED_DIR = os.path.join(MODEL_DIR, "trained")
EVAL_DIR = os.path.join(MODEL_DIR, "evaluation")

def train_treatment_recommendation_model():
    """Train treatment recommendation model"""
    print("Training treatment recommendation model...")
    
    # Prepare data
    X, y = prepare_training_data(SYNTHETIC_DIR)
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    
    # Create directories if they don't exist
    os.makedirs(TRAINED_DIR, exist_ok=True)
    os.makedirs(EVAL_DIR, exist_ok=True)
    
    # Try different models
    models = {
        'random_forest': RandomForestRegressor(
            n_estimators=100, max_depth=10, random_state=42
        ),
        'gradient_boosting': GradientBoostingRegressor(
            n_estimators=100, learning_rate=0.1, max_depth=5, random_state=42
        ),
        'xgboost': xgb.XGBRegressor(
            n_estimators=100, learning_rate=0.1, max_depth=5, random_state=42
        ),
        'linear_regression': LinearRegression()
    }
    
    results = []
    
    for name, model in models.items():
        print(f"Training {name}...")
        model.fit(X_train, y_train)
        
        # Predict
        y_pred = model.predict(X_test)
        
        # Evaluate
        mse = mean_squared_error(y_test, y_pred)
        mae = mean_absolute_error(y_test, y_pred)
        r2 = r2_score(y_test, y_pred)
        
        print(f"{name} - MSE: {mse:.4f}, MAE: {mae:.4f}, R²: {r2:.4f}")
        
        # Save results
        results.append({
            'model': name,
            'mse': mse,
            'mae': mae,
            'r2': r2
        })
        
        # Save model
        with open(os.path.join(TRAINED_DIR, f"{name}_recommendation.pkl"), 'wb') as f:
            pickle.dump(model, f)
            
        # Plot predictions vs actual
        plt.figure(figsize=(10, 6))
        plt.scatter(y_test, y_pred, alpha=0.5)
        plt.plot([0, 1], [0, 1], 'r--')
        plt.xlabel('Actual Effectiveness')
        plt.ylabel('Predicted Effectiveness')
        plt.title(f'{name} - Predicted vs Actual Effectiveness')
        plt.savefig(os.path.join(EVAL_DIR, f"{name}_recommendation_pred_vs_actual.png"))
        plt.close()
    
    # Save evaluation results
    results_df = pd.DataFrame(results)
    results_df.to_csv(os.path.join(EVAL_DIR, "recommendation_model_results.csv"), index=False)
    
    # Select best model
    best_model_name = results_df.loc[results_df['r2'].idxmax()]['model']
    with open(os.path.join(TRAINED_DIR, f"{best_model_name}_recommendation.pkl"), 'rb') as f:
        best_model = pickle.load(f)
    
    # Save as best model
    with open(os.path.join(TRAINED_DIR, "best_recommendation_model.pkl"), 'wb') as f:
        pickle.dump(best_model, f)
    
    # Save model type
    with open(os.path.join(TRAINED_DIR, "best_recommendation_model_type.txt"), 'w') as f:
        f.write(best_model_name)
    
    print(f"Best model: {best_model_name}")
    print("Treatment recommendation model trained successfully!")
    return best_model

def train_side_effect_prediction_model():
    """Train side effect prediction model"""
    print("Training side effect prediction model...")
    
    # Load synthetic side effect data
    side_effects_df = pd.read_csv(os.path.join(SYNTHETIC_DIR, "side_effects.csv"))
    medications_df = pd.read_csv(os.path.join(SYNTHETIC_DIR, "medications.csv"))
    
    # Merge data
    side_effect_data = pd.merge(
        side_effects_df,
        medications_df[['id', 'name']],
        left_on='medication_id',
        right_on='id',
        suffixes=('_se', '_med'),
        how='inner'
    )
    
    # Feature engineering
    from sklearn.preprocessing import OneHotEncoder
    
    # One-hot encode medication names
    medication_encoder = OneHotEncoder(sparse_output=False)
    medication_encoded = medication_encoder.fit_transform(side_effect_data[['name']])
    
    # Create features and targets
    X = medication_encoded
    y_severity = side_effect_data['severity'].values
    y_frequency = side_effect_data['frequency'].values
    
    # Split data
    X_train, X_test, y_severity_train, y_severity_test = train_test_split(
        X, y_severity, test_size=0.2, random_state=42
    )
    _, _, y_frequency_train, y_frequency_test = train_test_split(
        X, y_frequency, test_size=0.2, random_state=42
    )
    
    # Train severity model
    severity_model = GradientBoostingRegressor(
        n_estimators=100, learning_rate=0.1, max_depth=3, random_state=42
    )
    severity_model.fit(X_train, y_severity_train)
    
    # Train frequency model
    frequency_model = GradientBoostingRegressor(
        n_estimators=100, learning_rate=0.1, max_depth=3, random_state=42
    )
    frequency_model.fit(X_train, y_frequency_train)
    
    # Evaluate severity model
    y_severity_pred = severity_model.predict(X_test)
    severity_mse = mean_squared_error(y_severity_test, y_severity_pred)
    severity_mae = mean_absolute_error(y_severity_test, y_severity_pred)
    severity_r2 = r2_score(y_severity_test, y_severity_pred)
    
    print(f"Severity model - MSE: {severity_mse:.4f}, MAE: {severity_mae:.4f}, R²: {severity_r2:.4f}")
    
    # Evaluate frequency model
    y_frequency_pred = frequency_model.predict(X_test)
    frequency_mse = mean_squared_error(y_frequency_test, y_frequency_pred)
    frequency_mae = mean_absolute_error(y_frequency_test, y_frequency_pred)
    frequency_r2 = r2_score(y_frequency_test, y_frequency_pred)
    
    print(f"Frequency model - MSE: {frequency_mse:.4f}, MAE: {frequency_mae:.4f}, R²: {frequency_r2:.4f}")
    
    # Save models
    os.makedirs(TRAINED_DIR, exist_ok=True)
    
    with open(os.path.join(TRAINED_DIR, "side_effect_severity_model.pkl"), 'wb') as f:
        pickle.dump(severity_model, f)
    
    with open(os.path.join(TRAINED_DIR, "side_effect_frequency_model.pkl"), 'wb') as f:
        pickle.dump(frequency_model, f)
    
    # Save medication encoder
    with open(os.path.join(TRAINED_DIR, "medication_encoder.pkl"), 'wb') as f:
        pickle.dump(medication_encoder, f)
    
    # Save side effect names
    side_effect_names = side_effect_data[['name_se']].drop_duplicates()
    side_effect_names.to_csv(os.path.join(TRAINED_DIR, "side_effect_names.csv"), index=False)
    
    print("Side effect prediction models trained successfully!")
    return severity_model, frequency_model

def main():
    """Train all models"""
    os.makedirs(TRAINED_DIR, exist_ok=True)
    os.makedirs(EVAL_DIR, exist_ok=True)
    
    # Train models
    treatment_model = train_treatment_recommendation_model()
    severity_model, frequency_model = train_side_effect_prediction_model()
    
    print("All models trained successfully!")

if __name__ == "__main__":
    main()
