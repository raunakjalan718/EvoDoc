import os
import pandas as pd
import numpy as np
from faker import Faker
import random
from datetime import datetime, timedelta

# Paths
DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "data")
SYNTHETIC_DIR = os.path.join(DATA_DIR, "synthetic")

# Initialize faker
fake = Faker()

def generate_patients(n=100):
    """Generate synthetic patient data"""
    patients = []
    
    for i in range(1, n+1):
        gender = random.choice(['Male', 'Female'])
        if gender == 'Male':
            name = fake.name_male()
        else:
            name = fake.name_female()
            
        age = random.randint(18, 85)
        
        # Generate medical history based on age
        conditions = []
        if age > 50:
            if random.random() > 0.6:
                conditions.append("Hypertension")
            if random.random() > 0.7:
                conditions.append("Diabetes Type 2")
            if random.random() > 0.8:
                conditions.append("Hyperlipidemia")
        
        if random.random() > 0.8:
            conditions.append("Asthma")
        if random.random() > 0.9:
            conditions.append("Allergic Rhinitis")
            
        medical_history = ", ".join(conditions) if conditions else "No significant history"
        
        patients.append({
            'id': i,
            'name': name,
            'age': age,
            'gender': gender,
            'medical_history': medical_history,
            'created_at': fake.date_time_between(start_date='-1y', end_date='now').isoformat()
        })
    
    return pd.DataFrame(patients)

def generate_allergies():
    """Generate common allergies"""
    allergies = [
        {'id': 1, 'name': 'Penicillin', 'description': 'Allergy to penicillin-based antibiotics'},
        {'id': 2, 'name': 'Sulfa drugs', 'description': 'Allergy to sulfonamide medications'},
        {'id': 3, 'name': 'Aspirin', 'description': 'Allergy to aspirin and related compounds'},
        {'id': 4, 'name': 'NSAIDs', 'description': 'Allergy to non-steroidal anti-inflammatory drugs'},
        {'id': 5, 'name': 'Shellfish', 'description': 'Allergy to shellfish proteins'},
        {'id': 6, 'name': 'Nuts', 'description': 'Allergy to tree nuts or peanuts'},
        {'id': 7, 'name': 'Latex', 'description': 'Allergy to latex rubber proteins'},
        {'id': 8, 'name': 'Contrast Dye', 'description': 'Allergy to radiographic contrast materials'},
        {'id': 9, 'name': 'Eggs', 'description': 'Allergy to egg proteins'},
        {'id': 10, 'name': 'Dairy', 'description': 'Allergy or intolerance to dairy products'}
    ]
    return pd.DataFrame(allergies)

def generate_medications():
    """Generate common medications"""
    medications = [
        {'id': 1, 'name': 'Lisinopril', 'description': 'ACE inhibitor for hypertension', 'typical_dosage': '10-40mg daily'},
        {'id': 2, 'name': 'Atorvastatin', 'description': 'Statin for cholesterol reduction', 'typical_dosage': '10-80mg daily'},
        {'id': 3, 'name': 'Metformin', 'description': 'First-line medication for type 2 diabetes', 'typical_dosage': '500-2000mg daily'},
        {'id': 4, 'name': 'Amoxicillin', 'description': 'Penicillin antibiotic', 'typical_dosage': '250-500mg three times daily'},
        {'id': 5, 'name': 'Azithromycin', 'description': 'Macrolide antibiotic', 'typical_dosage': '500mg on day 1, then 250mg daily'},
        {'id': 6, 'name': 'Albuterol', 'description': 'Bronchodilator for asthma', 'typical_dosage': '1-2 puffs every 4-6 hours as needed'},
        {'id': 7, 'name': 'Levothyroxine', 'description': 'Thyroid hormone replacement', 'typical_dosage': '25-200mcg daily'},
        {'id': 8, 'name': 'Amlodipine', 'description': 'Calcium channel blocker for hypertension', 'typical_dosage': '5-10mg daily'},
        {'id': 9, 'name': 'Omeprazole', 'description': 'Proton pump inhibitor for acid reflux', 'typical_dosage': '20-40mg daily'},
        {'id': 10, 'name': 'Ibuprofen', 'description': 'NSAID for pain and inflammation', 'typical_dosage': '200-800mg every 4-6 hours'}
    ]
    return pd.DataFrame(medications)

def generate_ingredients():
    """Generate medication ingredients"""
    ingredients = [
        {'id': 1, 'name': 'Lisinopril', 'description': 'Active ingredient in ACE inhibitors'},
        {'id': 2, 'name': 'Atorvastatin calcium', 'description': 'Active ingredient in statins'},
        {'id': 3, 'name': 'Metformin hydrochloride', 'description': 'Active ingredient in diabetic medications'},
        {'id': 4, 'name': 'Amoxicillin trihydrate', 'description': 'Active ingredient in penicillin antibiotics'},
        {'id': 5, 'name': 'Azithromycin dihydrate', 'description': 'Active ingredient in macrolide antibiotics'},
        {'id': 6, 'name': 'Salbutamol sulfate', 'description': 'Active ingredient in albuterol inhalers'},
        {'id': 7, 'name': 'Levothyroxine sodium', 'description': 'Synthetic thyroid hormone'},
        {'id': 8, 'name': 'Amlodipine besylate', 'description': 'Active ingredient in calcium channel blockers'},
        {'id': 9, 'name': 'Omeprazole magnesium', 'description': 'Active ingredient in proton pump inhibitors'},
        {'id': 10, 'name': 'Ibuprofen', 'description': 'Active ingredient in NSAIDs'},
        {'id': 11, 'name': 'Lactose', 'description': 'Common filler in medications'},
        {'id': 12, 'name': 'Magnesium stearate', 'description': 'Common lubricant in tablet manufacturing'},
        {'id': 13, 'name': 'Povidone', 'description': 'Binding agent in tablets'},
        {'id': 14, 'name': 'Titanium dioxide', 'description': 'Coloring agent in medications'},
        {'id': 15, 'name': 'Gelatin', 'description': 'Used in capsule shells'}
    ]
    return pd.DataFrame(ingredients)

def generate_medication_ingredient_mapping():
    """Generate mapping between medications and ingredients"""
    mappings = [
        {'medication_id': 1, 'ingredient_id': 1},  # Lisinopril
        {'medication_id': 1, 'ingredient_id': 11},  # Lisinopril contains lactose
        {'medication_id': 1, 'ingredient_id': 12},  # Lisinopril contains magnesium stearate
        {'medication_id': 2, 'ingredient_id': 2},  # Atorvastatin
        {'medication_id': 2, 'ingredient_id': 11},
        {'medication_id': 2, 'ingredient_id': 12},
        {'medication_id': 3, 'ingredient_id': 3},  # Metformin
        {'medication_id': 3, 'ingredient_id': 13},
        {'medication_id': 4, 'ingredient_id': 4},  # Amoxicillin
        {'medication_id': 4, 'ingredient_id': 11},
        {'medication_id': 5, 'ingredient_id': 5},  # Azithromycin
        {'medication_id': 5, 'ingredient_id': 14},
        {'medication_id': 6, 'ingredient_id': 6},  # Albuterol
        {'medication_id': 7, 'ingredient_id': 7},  # Levothyroxine
        {'medication_id': 7, 'ingredient_id': 11},
        {'medication_id': 8, 'ingredient_id': 8},  # Amlodipine
        {'medication_id': 8, 'ingredient_id': 12},
        {'medication_id': 9, 'ingredient_id': 9},  # Omeprazole
        {'medication_id': 9, 'ingredient_id': 15},
        {'medication_id': 10, 'ingredient_id': 10},  # Ibuprofen
        {'medication_id': 10, 'ingredient_id': 12},
        {'medication_id': 10, 'ingredient_id': 13}
    ]
    return pd.DataFrame(mappings)

def generate_allergy_ingredient_mapping():
    """Generate mapping between allergies and ingredients"""
    mappings = [
        {'allergy_id': 1, 'ingredient_id': 4},  # Penicillin allergy - amoxicillin
        {'allergy_id': 2, 'ingredient_id': 5},  # Sulfa drugs
        {'allergy_id': 3, 'ingredient_id': 10},  # Aspirin - ibuprofen (related)
        {'allergy_id': 4, 'ingredient_id': 10},  # NSAIDs - ibuprofen
        {'allergy_id': 7, 'ingredient_id': 15},  # Latex - gelatin (simplified)
        {'allergy_id': 9, 'ingredient_id': 15},  # Eggs - gelatin (simplified)
        {'allergy_id': 10, 'ingredient_id': 11}  # Dairy - lactose
    ]
    return pd.DataFrame(mappings)

def generate_side_effects():
    """Generate side effects for medications"""
    side_effects = []
    side_effect_id = 1
    
    medication_side_effects = {
        1: [  # Lisinopril
            ("Dry cough", 0.15, 3),
            ("Dizziness", 0.08, 4),
            ("Headache", 0.05, 2),
            ("Hyperkalemia", 0.02, 6)
        ],
        2: [  # Atorvastatin
            ("Muscle pain", 0.10, 4),
            ("Liver enzyme elevation", 0.03, 5),
            ("Headache", 0.05, 2),
            ("Insomnia", 0.02, 3)
        ],
        3: [  # Metformin
            ("Diarrhea", 0.20, 3),
            ("Nausea", 0.15, 3),
            ("Vitamin B12 deficiency", 0.04, 4),
            ("Metallic taste", 0.08, 2)
        ],
        4: [  # Amoxicillin
            ("Diarrhea", 0.12, 3),
            ("Rash", 0.08, 4),
            ("Nausea", 0.06, 2),
            ("Candidiasis", 0.03, 4)
        ],
        5: [  # Azithromycin
            ("Diarrhea", 0.10, 3),
            ("Nausea", 0.07, 2),
            ("QT prolongation", 0.01, 7),
            ("Abdominal pain", 0.05, 3)
        ],
        6: [  # Albuterol
            ("Tremor", 0.15, 3),
            ("Tachycardia", 0.08, 4),
            ("Headache", 0.06, 2),
            ("Nervousness", 0.12, 3)
        ],
        7: [  # Levothyroxine
            ("Palpitations", 0.04, 4),
            ("Insomnia", 0.03, 3),
            ("Weight loss", 0.03, 2),
            ("Anxiety", 0.05, 3)
        ],
        8: [  # Amlodipine
            ("Peripheral edema", 0.12, 3),
            ("Headache", 0.06, 2),
            ("Dizziness", 0.04, 3),
            ("Flushing", 0.08, 2)
        ],
        9: [  # Omeprazole
            ("Headache", 0.07, 2),
            ("Diarrhea", 0.06, 3),
            ("Vitamin B12 deficiency", 0.03, 4),
            ("Increased fracture risk", 0.02, 5)
        ],
        10: [  # Ibuprofen
            ("Stomach pain", 0.10, 4),
            ("Heartburn", 0.12, 3),
            ("Dizziness", 0.05, 3),
            ("Edema", 0.04, 4),
            ("GI bleeding", 0.01, 8)
        ]
    }
    
    for med_id, effects in medication_side_effects.items():
        for name, frequency, severity in effects:
            side_effects.append({
                'id': side_effect_id,
                'medication_id': med_id,
                'name': name,
                'description': f"Common side effect of medication",
                'frequency': frequency,
                'severity': severity
            })
            side_effect_id += 1
    
    return pd.DataFrame(side_effects)

def generate_doctors(n=10):
    """Generate doctor data"""
    specializations = [
        "Family Medicine", "Internal Medicine", "Cardiology", "Endocrinology", 
        "Gastroenterology", "Pulmonology", "Nephrology", "Neurology",
        "Oncology", "Rheumatology"
    ]
    
    doctors = []
    for i in range(1, n+1):
        doctors.append({
            'id': i,
            'name': fake.name(),
            'specialization': random.choice(specializations),
            'created_at': fake.date_time_between(start_date='-2y', end_date='-6m').isoformat()
        })
    
    return pd.DataFrame(doctors)

def generate_patient_allergy_mapping(patients, allergies, seed=42):
    """Generate mapping between patients and allergies"""
    random.seed(seed)
    mappings = []
    
    for patient_id in patients['id']:
        # 40% chance of having at least one allergy
        if random.random() < 0.4:
            num_allergies = random.randint(1, 3)  # 1-3 allergies per patient
            patient_allergies = random.sample(list(allergies['id']), min(num_allergies, len(allergies)))
            
            for allergy_id in patient_allergies:
                mappings.append({
                    'patient_id': patient_id,
                    'allergy_id': allergy_id
                })
    
    return pd.DataFrame(mappings)

def generate_appointments(patients, doctors, seed=42):
    """Generate appointment data"""
    random.seed(seed)
    appointments = []
    appointment_id = 1
    
    # Common symptoms for appointments
    symptom_sets = [
        "Fever, cough, sore throat",
        "Headache, dizziness",
        "Chest pain, shortness of breath",
        "Abdominal pain, nausea",
        "Back pain, stiffness",
        "Rash, itching",
        "Fatigue, weight loss",
        "Anxiety, insomnia",
        "Joint pain, swelling",
        "Runny nose, sneezing, congestion"
    ]
    
    # Generate 1-3 appointments for each patient
    for patient_id in patients['id']:
        num_appointments = random.randint(1, 3)
        
        for _ in range(num_appointments):
            doctor_id = random.choice(doctors['id'])
            
            # Generate appointment date (past, present, future)
            time_choice = random.random()
            if time_choice < 0.6:  # 60% past appointments
                date = fake.date_time_between(start_date='-6m', end_date='-1d').isoformat()
                status = random.choices(['completed', 'cancelled'], weights=[0.9, 0.1])[0]
            elif time_choice < 0.9:  # 30% upcoming appointments
                date = fake.date_time_between(start_date='+1d', end_date='+1m').isoformat()
                status = 'scheduled'
            else:  # 10% today's appointments
                date = fake.date_time_between(start_date='now', end_date='+1d').isoformat()
                status = random.choice(['scheduled', 'in-progress'])
            
            appointments.append({
                'id': appointment_id,
                'patient_id': patient_id,
                'doctor_id': doctor_id,
                'date': date,
                'symptoms': random.choice(symptom_sets),
                'status': status,
                'created_at': fake.date_time_between(start_date='-6m', end_date='now').isoformat()
            })
            
            appointment_id += 1
    
    return pd.DataFrame(appointments)

def generate_treatments(appointments, medications, seed=42):
    """Generate treatment data"""
    random.seed(seed)
    treatments = []
    treatment_id = 1
    
    # Only generate treatments for completed appointments
    completed_appointments = appointments[appointments['status'] == 'completed']
    
    for _, appointment in completed_appointments.iterrows():
        # 1-3 medications per treatment
        num_medications = random.randint(1, 3)
        med_ids = random.sample(list(medications['id']), num_medications)
        
        for med_id in med_ids:
            # Get medication's typical dosage
            med_info = medications[medications['id'] == med_id].iloc[0]
            
            # Parse typical dosage (simplified)
            if 'mg' in med_info['typical_dosage']:
                dosage = med_info['typical_dosage'].split('mg')[0].split('-')[-1].strip() + ' mg'
            elif 'mcg' in med_info['typical_dosage']:
                dosage = med_info['typical_dosage'].split('mcg')[0].split('-')[-1].strip() + ' mcg'
            else:
                dosage = "Standard dose"
            
            # Generate frequencies
            frequencies = ["once daily", "twice daily", "three times daily", "four times daily", "as needed"]
            frequency = random.choice(frequencies)
            
            # Generate instructions
            instructions = random.choice([
                "Take with food",
                "Take on an empty stomach",
                "Take before bedtime",
                "Take in the morning",
                "Avoid alcohol while taking this medication",
                "Drink plenty of water with this medication",
                "Continue until prescription is finished"
            ])
            
            # Generate treatment dates
            appointment_date = datetime.fromisoformat(appointment['date'])
            start_date = appointment_date.strftime('%Y-%m-%d')
            
            # End date 7-14 days after start
            days_of_treatment = random.randint(7, 14)
            end_date = (appointment_date + timedelta(days=days_of_treatment)).strftime('%Y-%m-%d')
            
            treatments.append({
                'id': treatment_id,
                'appointment_id': appointment['id'],
                'doctor_id': appointment['doctor_id'],
                'medication_id': med_id,
                'dosage': dosage,
                'frequency': frequency,
                'instructions': instructions,
                'start_date': start_date,
                'end_date': end_date,
                'created_at': appointment['date']
            })
            
            treatment_id += 1
    
    return pd.DataFrame(treatments)

def generate_treatment_feedbacks(treatments, patients, seed=42):
    """Generate treatment feedback data"""
    random.seed(seed)
    feedbacks = []
    feedback_id = 1
    
    # Generate feedback for 80% of treatments
    for _, treatment in treatments.iterrows():
        if random.random() < 0.8:
            # Get appointment and patient information
            appointment_id = treatment['appointment_id']
            
            # Lookup patient_id from appointments table
            # Note: In a real system, this would be a database join
            # For this synthetic data, we'll simplify and use the treatment's first digit
            # as the patient_id (this is just a hack for synthetic data)
            patient_id = int(str(appointment_id)[0])
            
            # Ensure patient_id is valid
            if patient_id not in patients['id'].values:
                patient_id = random.choice(patients['id'].values)
            
            # Effectiveness rating (1-10)
            effectiveness = random.randint(3, 10)  # Bias toward positive results
            
            # Side effects (more likely if effectiveness is lower)
            side_effect_probability = 0.8 - (effectiveness / 15)  # 13% to 73% chance
            
            side_effects = ""
            if random.random() < side_effect_probability:
                possible_side_effects = [
                    "Nausea", "Headache", "Dizziness", "Fatigue", "Rash",
                    "Stomach pain", "Insomnia", "Dry mouth", "Diarrhea", "Constipation"
                ]
                num_side_effects = random.randint(1, 3)
                selected_side_effects = random.sample(possible_side_effects, num_side_effects)
                side_effects = ", ".join(selected_side_effects)
            
            # Comments
            if effectiveness >= 8:
                comments = random.choice([
                    "Worked very well, no issues",
                    "Symptoms improved quickly",
                    "Very satisfied with this treatment",
                    "Will recommend to others with similar condition",
                    ""
                ])
            elif effectiveness >= 5:
                comments = random.choice([
                    "Worked adequately but took time",
                    "Some improvement but not complete resolution",
                    "Acceptable results overall",
                    "Moderate improvement in symptoms",
                    ""
                ])
            else:
                comments = random.choice([
                    "Did not work well for me",
                    "Side effects were bothersome",
                    "Had to stop early due to side effects",
                    "Minimal improvement in symptoms",
                    "Would prefer to try something else",
                    ""
                ])
            
            feedbacks.append({
                'id': feedback_id,
                'treatment_id': treatment['id'],
                'patient_id': patient_id,
                'effectiveness': effectiveness,
                'side_effects': side_effects,
                'comments': comments,
                'created_at': (datetime.fromisoformat(treatment['end_date']) + timedelta(days=random.randint(1, 5))).isoformat()
            })
            
            feedback_id += 1
    
    return pd.DataFrame(feedbacks)

def main():
    """Generate all synthetic data"""
    print("Generating synthetic data...")
    
    # Create directory if it doesn't exist
    os.makedirs(SYNTHETIC_DIR, exist_ok=True)
    
    # Generate data
    patients_df = generate_patients(100)
    allergies_df = generate_allergies()
    medications_df = generate_medications()
    ingredients_df = generate_ingredients()
    medication_ingredient_df = generate_medication_ingredient_mapping()
    allergy_ingredient_df = generate_allergy_ingredient_mapping()
    side_effects_df = generate_side_effects()
    doctors_df = generate_doctors(10)
    patient_allergy_df = generate_patient_allergy_mapping(patients_df, allergies_df)
    appointments_df = generate_appointments(patients_df, doctors_df)
    treatments_df = generate_treatments(appointments_df, medications_df)
    feedbacks_df = generate_treatment_feedbacks(treatments_df, patients_df)
    
    # Save data
    patients_df.to_csv(os.path.join(SYNTHETIC_DIR, "patients.csv"), index=False)
    allergies_df.to_csv(os.path.join(SYNTHETIC_DIR, "allergies.csv"), index=False)
    medications_df.to_csv(os.path.join(SYNTHETIC_DIR, "medications.csv"), index=False)
    ingredients_df.to_csv(os.path.join(SYNTHETIC_DIR, "ingredients.csv"), index=False)
    medication_ingredient_df.to_csv(os.path.join(SYNTHETIC_DIR, "medication_ingredient.csv"), index=False)
    allergy_ingredient_df.to_csv(os.path.join(SYNTHETIC_DIR, "allergy_ingredient.csv"), index=False)
    side_effects_df.to_csv(os.path.join(SYNTHETIC_DIR, "side_effects.csv"), index=False)
    doctors_df.to_csv(os.path.join(SYNTHETIC_DIR, "doctors.csv"), index=False)
    patient_allergy_df.to_csv(os.path.join(SYNTHETIC_DIR, "patient_allergy.csv"), index=False)
    appointments_df.to_csv(os.path.join(SYNTHETIC_DIR, "appointments.csv"), index=False)
    treatments_df.to_csv(os.path.join(SYNTHETIC_DIR, "treatments.csv"), index=False)
    feedbacks_df.to_csv(os.path.join(SYNTHETIC_DIR, "treatment_feedbacks.csv"), index=False)
    
    print("Synthetic data generated successfully!")

if __name__ == "__main__":
    main()
