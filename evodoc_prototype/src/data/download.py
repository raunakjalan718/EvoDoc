import os
import pandas as pd
import requests
from zipfile import ZipFile
from io import BytesIO

# Paths
DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "data")
RAW_DIR = os.path.join(DATA_DIR, "raw")

def download_drug_review_dataset():
    """Download UCI ML Drug Review dataset"""
    url = "https://archive.ics.uci.edu/ml/machine-learning-databases/00462/drugsCom_raw.zip"
    print(f"Downloading Drug Review Dataset from {url}...")
    
    # Create directory if it doesn't exist
    os.makedirs(RAW_DIR, exist_ok=True)
    
    # Download and extract dataset
    response = requests.get(url)
    with ZipFile(BytesIO(response.content)) as zip_file:
        zip_file.extractall(RAW_DIR)
    
    print("Drug Review Dataset downloaded and extracted successfully.")

def download_faers_data():
    """Download a sample of FDA Adverse Event Reporting System data"""
    # Note: Full FAERS data is very large, this is a simplified approach for the prototype
    url = "https://api.fda.gov/drug/event.json?limit=1000"
    print(f"Downloading FDA Adverse Event sample data...")
    
    response = requests.get(url)
    data = response.json()
    
    # Save data to file
    faers_dir = os.path.join(RAW_DIR, "faers")
    os.makedirs(faers_dir, exist_ok=True)
    
    with open(os.path.join(faers_dir, "faers_sample.json"), "w") as f:
        import json
        json.dump(data, f)
    
    print("FAERS sample data downloaded successfully.")

def download_demo_mimic_data():
    """
    Note about MIMIC-III data:
    MIMIC-III requires credentialed access. For prototype purposes,
    we'll use a small sample of synthetic data based on MIMIC's structure.
    In a real project, you would need to apply for access through PhysioNet.
    """
    print("Creating synthetic MIMIC-like data for prototype...")
    
    # Create synthetic patients data (simplified MIMIC structure)
    patients = pd.DataFrame({
        'subject_id': range(1, 101),
        'gender': ['M', 'F'] * 50,
        'dob': pd.date_range(start='1940-01-01', periods=100, freq='100D'),
        'expire_flag': [0] * 90 + [1] * 10,
    })
    
    # Create synthetic admissions
    admissions = pd.DataFrame({
        'hadm_id': range(1, 151),
        'subject_id': [i for i in range(1, 101) for _ in range(1 + i % 2)],  # 1-2 admissions per patient
        'admittime': pd.date_range(start='2020-01-01', periods=150, freq='1D'),
        'dischtime': pd.date_range(start='2020-01-03', periods=150, freq='1D'),
        'diagnosis': ['Pneumonia', 'Heart Failure', 'Diabetes', 'Hypertension', 'Asthma'] * 30,
    })
    
    # Create synthetic prescriptions
    medications = ['Aspirin', 'Lisinopril', 'Metformin', 'Atorvastatin', 'Albuterol', 
                   'Paracetamol', 'Ibuprofen', 'Amoxicillin', 'Ciprofloxacin', 'Simvastatin']
    
    prescriptions = pd.DataFrame({
        'prescription_id': range(1, 301),
        'hadm_id': [i for i in range(1, 151) for _ in range(2)],  # 2 medications per admission
        'drug': [medications[i % len(medications)] for i in range(300)],
        'startdate': pd.date_range(start='2020-01-01', periods=300, freq='12H'),
        'enddate': pd.date_range(start='2020-01-05', periods=300, freq='12H'),
        'dose_val_rx': [str(i % 5 + 1) for i in range(300)],
        'dose_unit_rx': ['mg', 'g', 'ml', 'mcg', 'mg'] * 60,
    })
    
    # Save synthetic data
    mimic_dir = os.path.join(RAW_DIR, "mimic")
    os.makedirs(mimic_dir, exist_ok=True)
    
    patients.to_csv(os.path.join(mimic_dir, "patients.csv"), index=False)
    admissions.to_csv(os.path.join(mimic_dir, "admissions.csv"), index=False)
    prescriptions.to_csv(os.path.join(mimic_dir, "prescriptions.csv"), index=False)
    
    print("Synthetic MIMIC-like data created successfully.")

def main():
    # Create data directories if they don't exist
    os.makedirs(DATA_DIR, exist_ok=True)
    
    # Download datasets
    download_drug_review_dataset()
    download_faers_data()
    download_demo_mimic_data()
    
    print("All datasets downloaded successfully!")

if __name__ == "__main__":
    main()
