import os
import json
import pandas as pd
import numpy as np
import requests
from pathlib import Path

# Constants
DATA_DIR = Path("./data")
DATA_DIR.mkdir(exist_ok=True)

def download_datasets(force=False):
    """Download all required medical datasets once"""
    print("===== EvoDoc Dataset Downloader =====")
    
    # Check if data already exists
    if os.path.exists(DATA_DIR / "download_complete.flag") and not force:
        print("Datasets already downloaded. Use --force to re-download.")
        return
    
    print("Downloading medical datasets...")
    
    # 1. Create enhanced side effect data
    print("Creating enhanced side effect data...")
    create_enhanced_side_effect_data()
    
    # 2. Get FDA adverse events data
    print("Downloading FDA adverse event data...")
    try:
        response = requests.get("https://api.fda.gov/drug/event.json?limit=1000")
        with open(DATA_DIR / "faers_sample.json", "w") as f:
            json.dump(response.json(), f)
        print("FDA data downloaded successfully")
    except Exception as e:
        print(f"Error downloading FDA data: {e}")
        create_sample_faers_data()
    
    # 3. Create improved DrugBank-like data
    print("Creating enhanced medication database...")
    create_enhanced_drugbank_data()
    
    # 4. Create improved MIMIC-like treatment data with stronger correlations
    print("Creating enhanced clinical data...")
    create_enhanced_mimic_data()
    
    # Create flag file to indicate download is complete
    with open(DATA_DIR / "download_complete.flag", "w") as f:
        f.write("Download completed on " + pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S"))
    
    print("All datasets prepared successfully!")

def create_enhanced_side_effect_data():
    """Create more realistic side effect data"""
    side_effects = []
    medications = ["Amoxicillin", "Lisinopril", "Azithromycin", "Ibuprofen", "Loratadine", 
                   "Metformin", "Citalopram", "Cetirizine"]
    
    # Map medications to common side effects with realistic frequencies
    medication_side_effects = {
        "Amoxicillin": [
            ("Diarrhea", 0.08, 4), 
            ("Nausea", 0.06, 3), 
            ("Rash", 0.05, 6)
        ],
        "Lisinopril": [
            ("Dry cough", 0.20, 4), 
            ("Dizziness", 0.08, 3), 
            ("Headache", 0.06, 2)
        ],
        "Azithromycin": [
            ("Diarrhea", 0.07, 3), 
            ("Nausea", 0.05, 3), 
            ("Abdominal pain", 0.04, 4)
        ],
        "Ibuprofen": [
            ("Stomach pain", 0.10, 5), 
            ("Heartburn", 0.08, 4), 
            ("Dizziness", 0.04, 3)
        ],
        "Loratadine": [
            ("Drowsiness", 0.08, 3), 
            ("Dry mouth", 0.06, 2), 
            ("Headache", 0.03, 2)
        ],
        "Metformin": [
            ("Diarrhea", 0.15, 4), 
            ("Nausea", 0.10, 4), 
            ("Abdominal discomfort", 0.08, 3)
        ],
        "Citalopram": [
            ("Insomnia", 0.10, 4), 
            ("Nausea", 0.08, 3), 
            ("Sexual dysfunction", 0.12, 6)
        ],
        "Cetirizine": [
            ("Drowsiness", 0.10, 3), 
            ("Dry mouth", 0.07, 2), 
            ("Fatigue", 0.05, 3)
        ]
    }
    
    # Create side effects with realistic patterns
    for medication in medications:
        if medication in medication_side_effects:
            for effect, frequency, severity in medication_side_effects[medication]:
                # Add some randomness to make the data more realistic
                freq_variation = np.random.uniform(-0.02, 0.02)
                sev_variation = np.random.randint(-1, 2)
                
                side_effects.append({
                    "medication": medication,
                    "side_effect": effect,
                    "frequency": max(0.01, min(0.3, frequency + freq_variation)),
                    "severity": max(1, min(10, severity + sev_variation))
                })
        else:
            # Fallback for medications without specified patterns
            n_effects = np.random.randint(2, 4)
            possible_effects = ["Nausea", "Headache", "Dizziness", "Fatigue", "Dry mouth"]
            selected_effects = np.random.choice(possible_effects, size=n_effects, replace=False)
            
            for effect in selected_effects:
                side_effects.append({
                    "medication": medication,
                    "side_effect": effect,
                    "frequency": np.random.uniform(0.03, 0.12),
                    "severity": np.random.randint(2, 6)
                })
    
    df = pd.DataFrame(side_effects)
    df.to_csv(DATA_DIR / "side_effects.csv", index=False)
    print(f"Created {len(side_effects)} realistic side effect records")

def create_sample_faers_data():
    """Create sample FDA adverse event data"""
    sample_data = {
        "meta": {"disclaimer": "Sample FDA adverse event data for prototype"},
        "results": []
    }
    
    medications = ["Amoxicillin", "Lisinopril", "Azithromycin", "Ibuprofen", "Loratadine"]
    reactions = ["Nausea", "Headache", "Dizziness", "Rash", "Fatigue", "Diarrhea"]
    
    for i in range(50):
        medication = np.random.choice(medications)
        reaction = np.random.choice(reactions)
        
        sample_data["results"].append({
            "patient": {
                "reaction": [{"reactionmeddrapt": reaction}],
                "drug": [{"medicinalproduct": medication}]
            }
        })
    
    with open(DATA_DIR / "faers_sample.json", "w") as f:
        json.dump(sample_data, f)

def create_enhanced_drugbank_data():
    """Create medication database with more detailed medical information"""
    drug_data = {
        "drugs": [
            {
                "name": "Amoxicillin",
                "description": "Penicillin antibiotic",
                "mechanism": "Inhibits bacterial cell wall synthesis by binding to PBPs",
                "indications": ["Bacterial infections", "Pneumonia", "Bronchitis", "Sinusitis"],
                "contraindications": ["Penicillin allergy", "Infectious mononucleosis"],
                "drug_class": "Penicillin antibiotic",
                "typical_dosage": "250-500mg three times daily",
                "ingredients": ["Amoxicillin trihydrate", "Sodium starch glycolate", "Magnesium stearate"],
                "first_line_for": ["Streptococcal pharyngitis", "Otitis media", "Uncomplicated UTI"]
            },
            {
                "name": "Lisinopril",
                "description": "ACE inhibitor for hypertension",
                "mechanism": "Inhibits angiotensin-converting enzyme, reducing angiotensin II production",
                "indications": ["Hypertension", "Heart failure", "Post-myocardial infarction"],
                "contraindications": ["Pregnancy", "History of angioedema", "ACE inhibitor allergy", "Bilateral renal artery stenosis"],
                "drug_class": "ACE inhibitor",
                "typical_dosage": "10-40mg once daily",
                "ingredients": ["Lisinopril dihydrate", "Calcium phosphate", "Magnesium stearate"],
                "first_line_for": ["Hypertension with diabetes", "Hypertension with heart failure", "Hypertension with kidney disease"]
            },
            {
                "name": "Azithromycin",
                "description": "Macrolide antibiotic",
                "mechanism": "Inhibits bacterial protein synthesis by binding to the 50S ribosomal subunit",
                "indications": ["Respiratory infections", "Skin infections", "STDs", "Strep throat"],
                "contraindications": ["Macrolide allergy", "Severe liver disease", "History of QT prolongation"],
                "drug_class": "Macrolide antibiotic",
                "typical_dosage": "500mg on day 1, then 250mg for 4 days",
                "ingredients": ["Azithromycin dihydrate", "Pregelatinized starch", "Magnesium stearate"],
                "first_line_for": ["Community-acquired pneumonia", "Acute bronchitis", "Chlamydial infections"]
            },
            {
                "name": "Ibuprofen",
                "description": "NSAID for pain and inflammation",
                "mechanism": "Inhibits COX enzymes reducing prostaglandin synthesis",
                "indications": ["Pain", "Inflammation", "Fever", "Menstrual cramps"],
                "contraindications": ["Aspirin allergy", "NSAID allergy", "Peptic ulcer", "Severe heart failure", "Third trimester pregnancy"],
                "drug_class": "NSAID",
                "typical_dosage": "200-800mg every 4-6 hours",
                "ingredients": ["Ibuprofen", "Microcrystalline cellulose", "Croscarmellose sodium"],
                "first_line_for": ["Mild to moderate pain", "Inflammatory conditions", "Fever"]
            },
            {
                "name": "Loratadine",
                "description": "Second-generation antihistamine for allergies",
                "mechanism": "H1 receptor antagonist with minimal sedation",
                "indications": ["Allergic rhinitis", "Urticaria", "Seasonal allergies"],
                "contraindications": ["Antihistamine hypersensitivity"],
                "drug_class": "Second-generation antihistamine",
                "typical_dosage": "10mg once daily",
                "ingredients": ["Loratadine", "Lactose monohydrate", "Magnesium stearate"],
                "first_line_for": ["Seasonal allergies", "Chronic urticaria"]
            },
            {
                "name": "Metformin",
                "description": "Biguanide antidiabetic",
                "mechanism": "Decreases hepatic glucose production and improves insulin sensitivity",
                "indications": ["Type 2 diabetes mellitus", "Prediabetes", "PCOS"],
                "contraindications": ["Kidney disease", "Metabolic acidosis", "Severe liver disease"],
                "drug_class": "Biguanide",
                "typical_dosage": "500-1000mg twice daily",
                "ingredients": ["Metformin hydrochloride", "Povidone", "Magnesium stearate"],
                "first_line_for": ["Type 2 diabetes", "Insulin resistance"]
            },
            {
                "name": "Citalopram",
                "description": "SSRI antidepressant",
                "mechanism": "Selective serotonin reuptake inhibitor",
                "indications": ["Depression", "Anxiety disorders", "Panic disorder"],
                "contraindications": ["MAO inhibitor use", "QT interval prolongation", "Recent heart attack"],
                "drug_class": "SSRI",
                "typical_dosage": "20-40mg once daily",
                "ingredients": ["Citalopram hydrobromide", "Microcrystalline cellulose", "Lactose monohydrate"],
                "first_line_for": ["Major depressive disorder", "Generalized anxiety disorder"]
            },
            {
                "name": "Cetirizine",
                "description": "Second-generation antihistamine",
                "mechanism": "H1 receptor antagonist with minimal anticholinergic effects",
                "indications": ["Allergic rhinitis", "Urticaria", "Atopic dermatitis"],
                "contraindications": ["Antihistamine hypersensitivity", "Severe kidney disease"],
                "drug_class": "Second-generation antihistamine",
                "typical_dosage": "10mg once daily",
                "ingredients": ["Cetirizine hydrochloride", "Microcrystalline cellulose", "Lactose"],
                "first_line_for": ["Allergic rhinitis", "Chronic urticaria"]
            }
        ]
    }
    
    with open(DATA_DIR / "drugbank_sample.json", "w") as f:
        json.dump(drug_data, f, indent=2)
    
    # Create contraindications file for easier processing
    contraindications = []
    for drug in drug_data["drugs"]:
        for contraind in drug["contraindications"]:
            contraindications.append({
                "medication": drug["name"],
                "contraindication": contraind
            })
    
    pd.DataFrame(contraindications).to_csv(DATA_DIR / "contraindications.csv", index=False)
    
    # Create first-line treatment mapping for improved recommendations
    first_line_treatments = []
    for drug in drug_data["drugs"]:
        for condition in drug.get("first_line_for", []):
            first_line_treatments.append({
                "condition": condition,
                "medication": drug["name"],
                "drug_class": drug.get("drug_class", "")
            })
    
    pd.DataFrame(first_line_treatments).to_csv(DATA_DIR / "first_line_treatments.csv", index=False)
    
    print(f"Created enhanced database with {len(drug_data['drugs'])} medications, " 
          f"{len(contraindications)} contraindications, and {len(first_line_treatments)} first-line treatments")

def create_enhanced_mimic_data():
    """Create synthetic clinical treatment data with strong realistic correlations"""
    # Set random seed for reproducibility
    np.random.seed(42)
    
    # Generate synthetic patients
    n_patients = 200  # Increased from 100
    patient_ids = np.arange(1, n_patients + 1)
    
    # More balanced gender distribution
    genders = np.random.choice(['M', 'F'], size=n_patients, p=[0.5, 0.5])
    
    # More realistic age distribution
    ages = np.concatenate([
        np.random.normal(30, 8, size=n_patients//4),    # Young adults
        np.random.normal(45, 10, size=n_patients//4),   # Middle-aged
        np.random.normal(65, 8, size=n_patients//4),    # Senior
        np.random.uniform(18, 85, size=n_patients//4)   # Mix
    ])
    ages = np.clip(ages, 18, 95).astype(int)
    
    patients = pd.DataFrame({
        'subject_id': patient_ids,
        'gender': genders,
        'age': ages
    })
    
    # Generate synthetic diagnoses with comorbidity patterns
    diagnoses = []
    common_diagnoses = [
        "Hypertension", "Type 2 Diabetes", "Asthma", "COPD", 
        "Pneumonia", "Bronchitis", "Common Cold", "Influenza",
        "Urinary Tract Infection", "Gastroenteritis", "Migraine",
        "Osteoarthritis", "Depression", "Anxiety", "Allergic Rhinitis"
    ]
    
    # Create comorbidity patterns (certain conditions often occur together)
    comorbidity_groups = [
        ["Hypertension", "Type 2 Diabetes", "Osteoarthritis"],  # Metabolic syndrome cluster
        ["Asthma", "Allergic Rhinitis"],                        # Atopic cluster
        ["Depression", "Anxiety"],                              # Mental health cluster
        ["COPD", "Bronchitis"]                                  # Respiratory cluster
    ]
    
    for patient_id in patient_ids:
        # Get patient age for age-related conditions
        patient_age = patients[patients['subject_id'] == patient_id]['age'].values[0]
        
        # Determine number of diagnoses (older patients tend to have more)
        if patient_age > 65:
            n_diagnoses = np.random.randint(2, 6)  # More conditions for elderly
        elif patient_age > 40:
            n_diagnoses = np.random.randint(1, 4)  # Some conditions for middle-aged
        else:
            n_diagnoses = np.random.randint(1, 3)  # Fewer for young
            
        # Randomly choose whether to use a comorbidity group
        use_comorbidity = np.random.random() < 0.7  # 70% chance
        
        if use_comorbidity and n_diagnoses >= 2:
            # Select a random comorbidity group
            selected_group = np.random.choice(len(comorbidity_groups))
            # Take a subset of conditions from the group
            n_from_group = min(n_diagnoses, len(comorbidity_groups[selected_group]))
            selected_conditions = np.random.choice(comorbidity_groups[selected_group], 
                                                  size=n_from_group, replace=False)
            
            # Add these diagnoses
            for diagnosis in selected_conditions:
                diagnoses.append({
                    'subject_id': patient_id,
                    'diagnosis': diagnosis
                })
                
            # If we need more conditions, select from the common list
            remaining = n_diagnoses - n_from_group
            if remaining > 0:
                remaining_conditions = [d for d in common_diagnoses 
                                        if d not in comorbidity_groups[selected_group]]
                additional = np.random.choice(remaining_conditions, size=remaining, replace=False)
                for diagnosis in additional:
                    diagnoses.append({
                        'subject_id': patient_id,
                        'diagnosis': diagnosis
                    })
        else:
            # Just select random diagnoses
            selected_conditions = np.random.choice(common_diagnoses, size=n_diagnoses, replace=False)
            for diagnosis in selected_conditions:
                diagnoses.append({
                    'subject_id': patient_id,
                    'diagnosis': diagnosis
                })
    
    diagnoses_df = pd.DataFrame(diagnoses)
    
    # Define more realistic diagnosis-medication mappings with efficacy
    diagnosis_medications = {
        "Hypertension": [
            ("Lisinopril", 0.85), ("Amlodipine", 0.8), ("Hydrochlorothiazide", 0.75)
        ],
        "Type 2 Diabetes": [
            ("Metformin", 0.9), ("Glipizide", 0.7), ("Sitagliptin", 0.75)
        ],
        "Asthma": [
            ("Albuterol", 0.85), ("Fluticasone", 0.8), ("Montelukast", 0.7)
        ],
        "COPD": [
            ("Albuterol", 0.8), ("Tiotropium", 0.85), ("Budesonide", 0.75)
        ],
        "Pneumonia": [
            ("Amoxicillin", 0.85), ("Azithromycin", 0.8), ("Doxycycline", 0.75)
        ],
        "Bronchitis": [
            ("Amoxicillin", 0.8), ("Azithromycin", 0.85), ("Doxycycline", 0.7)
        ],
        "Common Cold": [
            ("Ibuprofen", 0.7), ("Acetaminophen", 0.7), ("Dextromethorphan", 0.6)
        ],
        "Influenza": [
            ("Oseltamivir", 0.8), ("Acetaminophen", 0.65), ("Dextromethorphan", 0.55)
        ],
        "Urinary Tract Infection": [
            ("Nitrofurantoin", 0.85), ("Ciprofloxacin", 0.8), ("Trimethoprim", 0.75)
        ],
        "Gastroenteritis": [
            ("Loperamide", 0.75), ("Bismuth subsalicylate", 0.7), ("Ondansetron", 0.8)
        ],
        "Migraine": [
            ("Sumatriptan", 0.85), ("Propranolol", 0.7), ("Topiramate", 0.75)
        ],
        "Osteoarthritis": [
            ("Ibuprofen", 0.75), ("Naproxen", 0.7), ("Celecoxib", 0.8)
        ],
        "Depression": [
            ("Citalopram", 0.8), ("Sertraline", 0.85), ("Escitalopram", 0.85)
        ],
        "Anxiety": [
            ("Citalopram", 0.75), ("Sertraline", 0.8), ("Escitalopram", 0.8)
        ],
        "Allergic Rhinitis": [
            ("Loratadine", 0.85), ("Cetirizine", 0.85), ("Fluticasone", 0.8)
        ]
    }
    
    # Generate synthetic treatments with realistic effectiveness patterns
    treatments = []
    
    for _, row in diagnoses_df.iterrows():
        patient_id = row['subject_id']
        diagnosis = row['diagnosis']
        patient_age = patients[patients['subject_id'] == patient_id]['age'].values[0]
        
        medications = diagnosis_medications.get(diagnosis, [("Ibuprofen", 0.6), ("Acetaminophen", 0.6)])
        
        # Select 1-3 medications based on diagnosis
        n_meds = np.random.randint(1, min(4, len(medications) + 1))
        selected_meds = np.random.choice(range(len(medications)), size=n_meds, replace=False)
        
        for med_idx in selected_meds:
            medication, base_effectiveness = medications[med_idx]
            
            # Apply age-based adjustments
            if patient_age > 70:
                # Elderly patients often have reduced effectiveness or more side effects
                age_factor = np.random.uniform(0.8, 0.95)
            elif patient_age < 25:
                # Young adults may respond differently
                age_factor = np.random.uniform(0.9, 1.05)
            else:
                # Middle-aged patients (the clinical trial demographic)
                age_factor = np.random.uniform(0.95, 1.05)
            
            # Apply some random variation, but maintain the relationship
            # between appropriate meds and conditions
            effectiveness = int(round(10 * base_effectiveness * age_factor * np.random.uniform(0.85, 1.15)))
            # Clamp to valid range
            effectiveness = max(1, min(10, effectiveness))
            
            treatments.append({
                'subject_id': patient_id,
                'diagnosis': diagnosis,
                'medication': medication,
                'effectiveness': effectiveness
            })
    
    # Add some inappropriate treatments with low effectiveness
    for i in range(int(len(treatments) * 0.15)):  # About 15% of the total treatments
        patient_id = np.random.choice(patient_ids)
        patient_age = patients[patients['subject_id'] == patient_id]['age'].values[0]
        
        # Get a random diagnosis and an inappropriate medication for it
        diagnosis = np.random.choice(common_diagnoses)
        
        # Get medications that are NOT indicated for this diagnosis
        appropriate_meds = [med for med, _ in diagnosis_medications.get(diagnosis, [])]
        all_meds = set()
        for med_list in diagnosis_medications.values():
            for med, _ in med_list:
                all_meds.add(med)
                
        inappropriate_meds = list(all_meds - set(appropriate_meds))
        
        if inappropriate_meds:
            medication = np.random.choice(inappropriate_meds)
            # Inappropriate medications have low effectiveness
            effectiveness = np.random.randint(1, 5)  # 1-4 out of 10
            
            treatments.append({
                'subject_id': patient_id,
                'diagnosis': diagnosis,
                'medication': medication,
                'effectiveness': effectiveness
            })
    
    treatments_df = pd.DataFrame(treatments)
    
    # Save synthetic data
    patients.to_csv(DATA_DIR / "patients.csv", index=False)
    diagnoses_df.to_csv(DATA_DIR / "diagnoses.csv", index=False)
    treatments_df.to_csv(DATA_DIR / "treatments.csv", index=False)
    
    # Create final combined treatment data
    treatment_data = pd.merge(
        treatments_df,
        patients,
        on="subject_id"
    )
    
    # Add domain knowledge features
    treatment_data['is_appropriate'] = treatment_data.apply(
        lambda row: 1 if any(row['medication'] == med 
                            for med, _ in diagnosis_medications.get(row['diagnosis'], []))
                   else 0,
        axis=1
    )
    
    # Age category feature
    treatment_data['age_group'] = pd.cut(
        treatment_data['age'], 
        bins=[0, 18, 40, 65, 100], 
        labels=['pediatric', 'young_adult', 'middle_age', 'elderly']
    )
    
    treatment_data.to_csv(DATA_DIR / "treatment_data.csv", index=False)
    print(f"Created enhanced clinical dataset with {len(treatment_data)} treatment records, "
          f"including {len(patients)} patients and {diagnoses_df['diagnosis'].nunique()} unique conditions")

if __name__ == "__main__":
    import sys
    force = "--force" in sys.argv
    download_datasets(force)
    print("Dataset download complete. Next, run train_models.py")
