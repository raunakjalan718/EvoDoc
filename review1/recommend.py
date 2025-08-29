import os
import pickle
import json
import numpy as np
import pandas as pd
import requests
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables (for API key)
load_dotenv()

# Constants
DATA_DIR = Path("./data")
MODELS_DIR = Path("./models")
KIMI_API_KEY = os.getenv("KIMI_API_KEY", "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")
KIMI_API_URL = "https://openrouter.ai/api/v1/chat/completions"

class TreatmentRecommender:
    def __init__(self):
        """Initialize the treatment recommender system"""
        # Check if models exist
        if not os.path.exists(MODELS_DIR / "models.pkl") or not os.path.exists(MODELS_DIR / "encoders.pkl"):
            print("Error: Model files not found. Please run train_models.py first.")
            exit(1)
            
        # Load models and encoders
        try:
            with open(MODELS_DIR / "models.pkl", "rb") as f:
                self.models = pickle.load(f)
            
            with open(MODELS_DIR / "encoders.pkl", "rb") as f:
                self.encoders = pickle.load(f)
                
            print("Models and encoders loaded successfully.")
        except Exception as e:
            print(f"Error loading models: {e}")
            exit(1)
            
        # Load contraindications data
        try:
            self.contraindications = pd.read_csv(DATA_DIR / "contraindications.csv")
            print(f"Loaded {len(self.contraindications)} contraindication records.")
        except Exception as e:
            print(f"Error loading contraindications: {e}")
            # Create empty dataframe with required columns as fallback
            self.contraindications = pd.DataFrame(columns=["medication", "contraindication"])
            
        # Load side effects data
        try:
            self.side_effects = pd.read_csv(DATA_DIR / "side_effects.csv")
            print(f"Loaded {len(self.side_effects)} side effect records.")
        except Exception as e:
            print(f"Error loading side effects: {e}")
            # Create empty dataframe with required columns as fallback
            self.side_effects = pd.DataFrame(columns=["medication", "side_effect", "frequency", "severity"])
        
        # Load drug data
        try:
            with open(DATA_DIR / "drugbank_sample.json", "r") as f:
                drug_data = json.load(f)
            self.drugs = {drug["name"]: drug for drug in drug_data["drugs"]}
            print(f"Loaded {len(self.drugs)} drug records.")
        except Exception as e:
            print(f"Error loading drug data: {e}")
            self.drugs = {}
        
        # Load first-line treatments if available
        try:
            self.first_line_treatments = pd.read_csv(DATA_DIR / "first_line_treatments.csv")
            print(f"Loaded {len(self.first_line_treatments)} first-line treatment records.")
            
            # Create a mapping for easy lookup
            self.first_line_map = {}
            for _, row in self.first_line_treatments.iterrows():
                condition = row['condition']
                medication = row['medication']
                if condition not in self.first_line_map:
                    self.first_line_map[condition] = []
                self.first_line_map[condition].append(medication)
        except:
            print("First-line treatment data not available.")
            self.first_line_treatments = None
            self.first_line_map = {}
        
    def get_recommendations(self, patient_info):
        """Generate treatment recommendations based on patient information"""
        # Extract patient data
        age = patient_info["age"]
        gender = patient_info["gender"]
        symptoms = patient_info["symptoms"]
        allergies = patient_info["allergies"]
        current_medications = patient_info["current_medications"]
        
        print(f"Generating recommendations for {patient_info['name']} ({age}, {gender})")
        print(f"Symptoms: {symptoms}")
        print(f"Allergies: {', '.join(allergies) if allergies else 'None reported'}")
        print(f"Current medications: {', '.join(current_medications) if current_medications else 'None'}")
        
        # Find most relevant diagnosis based on symptoms
        diagnosis = self._find_matching_diagnosis(symptoms)
        print(f"Matched symptoms to diagnosis: {diagnosis}")
        
        # Check for first-line treatments for this diagnosis
        first_line_options = []
        if diagnosis in self.first_line_map:
            first_line_options = self.first_line_map[diagnosis]
            print(f"Found {len(first_line_options)} first-line treatments for {diagnosis}")
        
        # Prepare features for prediction
        patient_features = self._prepare_patient_features(age, gender, diagnosis)
        
        # Get available medications for prediction
        try:
            all_medications = list(self.encoders["medication"].categories_[0])
            print(f"Found {len(all_medications)} medications in encoder.")
        except Exception as e:
            print(f"Error getting medications from encoder: {e}")
            # Fallback to a default list of common medications
            all_medications = ["Amoxicillin", "Lisinopril", "Azithromycin", "Ibuprofen", "Loratadine", 
                             "Metformin", "Citalopram", "Cetirizine"]
            print(f"Using fallback list of {len(all_medications)} medications.")
        
        # Predict effectiveness for each medication
        predictions = []
        
        for medication in all_medications:
            try:
                # Check medication details from drug database
                med_info = self.drugs.get(medication, {})
                med_class = med_info.get('drug_class', '')
                
                # Create medication feature
                med_feature = np.zeros((1, len(all_medications)))
                med_idx = np.where(np.array(all_medications) == medication)[0]
                
                if len(med_idx) > 0:
                    med_feature[0, med_idx[0]] = 1
                else:
                    print(f"Warning: Medication '{medication}' not found in encoder index.")
                    continue
                
                # Combine features
                X = np.hstack([
                    patient_features[:, :1],  # age
                    patient_features[:, 1:3],  # gender
                    patient_features[:, 3:],  # diagnosis
                    med_feature
                ])
                
                # Predict effectiveness
                effectiveness = float(self.models['recommendation'].predict(X)[0])
                
                # Apply first-line treatment bonus
                is_first_line = medication in first_line_options
                if is_first_line:
                    effectiveness = min(1.0, effectiveness * 1.15)  # 15% bonus for first-line
                
                # Check for contraindications based on allergies
                contraindicated = False
                contraindication_reason = None
                
                for allergy in allergies:
                    if not allergy:  # Skip empty strings
                        continue
                        
                    # Check if medication is contraindicated for this allergy
                    contra_matches = self.contraindications[
                        (self.contraindications['medication'] == medication) & 
                        (self.contraindications['contraindication'].str.contains(allergy, case=False, na=False))
                    ]
                    
                    if not contra_matches.empty:
                        contraindicated = True
                        contraindication_reason = f"Patient is allergic to {allergy}"
                        break
                    
                    # Also check if medication contains the allergen in its ingredients
                    if medication in self.drugs:
                        ingredients = self.drugs[medication].get('ingredients', [])
                        if any(allergy.lower() in ingredient.lower() for ingredient in ingredients):
                            contraindicated = True
                            contraindication_reason = f"Contains {allergy} or related compounds"
                            break
                
                # Check for drug interactions with current medications
                interaction_warning = None
                for current_med in current_medications:
                    # This is a simplified check - in a real system, you'd use a drug interaction database
                    if medication == "Citalopram" and current_med in ["Sertraline", "Escitalopram", "Fluoxetine"]:
                        interaction_warning = f"Potential serotonin syndrome risk with {current_med}"
                    elif medication == "Ibuprofen" and current_med in ["Aspirin", "Naproxen", "Warfarin"]:
                        interaction_warning = f"Increased bleeding risk with {current_med}"
                
                # Get side effects for this medication
                side_effects = self._get_side_effects(medication)
                
                predictions.append({
                    'medication': medication,
                    'drug_class': med_class,
                    'effectiveness': effectiveness,
                    'is_first_line': is_first_line,
                    'contraindicated': contraindicated,
                    'contraindication_reason': contraindication_reason,
                    'interaction_warning': interaction_warning,
                    'side_effects': side_effects
                })
            except Exception as e:
                print(f"Error processing medication '{medication}': {e}")
                continue
        
        # If no predictions were made, return an error message
        if not predictions:
            return {
                'diagnosis': diagnosis,
                'recommendations': [],
                'contraindications': [],
                'ai_insights': "No recommendations could be generated. The model may need to be retrained."
            }
        
        # Sort by effectiveness (contraindicated meds at the bottom)
        predictions.sort(key=lambda x: (x['contraindicated'], -x['effectiveness']))
        
        # Separate recommendations and contraindications
        recommendations = []
        contraindications = []
        
        for pred in predictions:
            if pred['contraindicated']:
                contraindications.append({
                    'medication': pred['medication'],
                    'drug_class': pred['drug_class'],
                    'reason': pred['contraindication_reason']
                })
            else:
                recommendations.append({
                    'medication': pred['medication'],
                    'drug_class': pred['drug_class'],
                    'effectiveness': pred['effectiveness'],
                    'is_first_line': pred['is_first_line'],
                    'interaction_warning': pred['interaction_warning'],
                    'side_effects': pred['side_effects']
                })
        
        # Get AI insights for the top recommendations
        ai_insights = self._get_kimi_insights(symptoms, diagnosis, allergies, current_medications, predictions[:3])
        
        return {
            'diagnosis': diagnosis,
            'recommendations': recommendations[:5],  # Top 5 safe recommendations
            'contraindications': contraindications,
            'ai_insights': ai_insights
        }
    
    def _find_matching_diagnosis(self, symptoms):
        """Find the most likely diagnosis based on symptoms"""
        try:
            # Get all possible diagnoses from the encoder
            all_diagnoses = list(self.encoders['diagnosis'].categories_[0])
            
            # Search for exact matches first
            for diagnosis in all_diagnoses:
                if symptoms.lower() in diagnosis.lower():
                    return diagnosis
            
            # Search for partial word matches
            symptom_words = set(symptoms.lower().split())
            best_match = None
            best_score = -1
            
            for diagnosis in all_diagnoses:
                diagnosis_words = set(diagnosis.lower().split())
                # Count word overlap
                overlap = len(symptom_words.intersection(diagnosis_words))
                if overlap > best_score:
                    best_score = overlap
                    best_match = diagnosis
            
            if best_score > 0:
                return best_match
            
            # If no match, use common symptom-condition mappings
            symptom_map = {
                'fever': ['Influenza', 'Pneumonia', 'Common Cold'],
                'cough': ['Bronchitis', 'Pneumonia', 'Common Cold', 'COPD'],
                'headache': ['Migraine', 'Hypertension', 'Common Cold'],
                'pain': ['Osteoarthritis', 'Migraine'],
                'rash': ['Allergic Rhinitis', 'Urticaria'],
                'breath': ['Asthma', 'COPD', 'Heart failure'],
                'chest': ['Heart failure', 'Pneumonia'],
                'blood pressure': ['Hypertension'],
                'sugar': ['Type 2 Diabetes'],
                'nausea': ['Gastroenteritis'],
                'diarrhea': ['Gastroenteritis'],
                'anxiety': ['Anxiety'],
                'depression': ['Depression'],
                'sad': ['Depression']
            }
            
            # Look for symptom keywords
            for keyword, possible_diagnoses in symptom_map.items():
                if keyword in symptoms.lower():
                    # Return the first diagnosis that exists in our encoder
                    for diag in possible_diagnoses:
                        if diag in all_diagnoses:
                            return diag
            
            # Last resort - return first common condition or "Common Cold" as fallback
            return next((diag for diag in ['Common Cold', 'Hypertension', 'Type 2 Diabetes'] 
                         if diag in all_diagnoses), all_diagnoses[0])
        except Exception as e:
            print(f"Error matching diagnosis: {e}")
            return "Common Cold"  # Default fallback
    
    def _prepare_patient_features(self, age, gender, diagnosis):
        """Prepare patient features for prediction"""
        # Scale age
        try:
            age_scaled = self.encoders['age'].transform([[age]])
        except Exception as e:
            print(f"Error scaling age: {e}")
            # Fallback to unscaled age as a simple column vector
            age_scaled = np.array([[age]]) / 100.0  # Simple scaling
        
        # Encode gender
        try:
            gender_encoded = self.encoders['gender'].transform([[gender]])
        except Exception as e:
            print(f"Error encoding gender: {e}")
            # Fallback to simple one-hot encoding
            gender_encoded = np.array([[1, 0]]) if gender == 'M' else np.array([[0, 1]])
        
        # Find most relevant diagnosis
        try:
            # Encode diagnosis
            diagnosis_encoded = self.encoders['diagnosis'].transform([[diagnosis]])
        except Exception as e:
            print(f"Error processing diagnosis: {e}")
            # Create a zero vector as fallback
            try:
                diagnosis_encoded = np.zeros((1, len(self.encoders['diagnosis'].categories_[0])))
            except:
                diagnosis_encoded = np.zeros((1, 10))  # Arbitrary size if we can't get the actual size
        
        # Combine features
        features = np.hstack([age_scaled, gender_encoded, diagnosis_encoded])
        return features
    
    def _get_side_effects(self, medication):
        """Get side effects for a medication"""
        # Check if we have side effects data for this medication
        try:
            med_side_effects = self.side_effects[self.side_effects['medication'] == medication]
            
            if not med_side_effects.empty:
                # Return actual side effects
                side_effects = []
                for _, row in med_side_effects.iterrows():
                    side_effects.append({
                        'name': row['side_effect'],
                        'frequency': row['frequency'],
                        'severity': row['severity'] / 10.0  # Normalize to 0-1
                    })
                return side_effects
            else:
                # Return empty list if no side effects data
                return []
        except Exception as e:
            print(f"Error getting side effects for {medication}: {e}")
            return []
    
    def _get_kimi_insights(self, symptoms, diagnosis, allergies, current_medications, top_recommendations):
        """Get additional insights from KimiAI via OpenRouter"""
        try:
            # Prepare top recommendations as text
            rec_text = ""
            for i, r in enumerate(top_recommendations[:3]):
                if not r['contraindicated']:
                    rec_text += f"- {r['medication']} ({r['drug_class']}): Effectiveness {r['effectiveness']:.0%}"
                    if r['is_first_line']:
                        rec_text += " (First-line treatment)"
                    rec_text += "\n"
                    
                    if r['interaction_warning']:
                        rec_text += f"  Warning: {r['interaction_warning']}\n"
                        
                    if r['side_effects']:
                        rec_text += "  Common side effects: "
                        rec_text += ", ".join(f"{se['name']} ({se['frequency']:.0%} frequency)" 
                                             for se in r['side_effects'][:3])
                        rec_text += "\n"
            
            if not rec_text:
                rec_text = "No suitable medications found."
            
            # Construct prompt
            prompt = f"""
            Based on the following patient information, provide a brief analysis of the treatment recommendations:
            
            PATIENT SYMPTOMS: {symptoms}
            DIAGNOSED CONDITION: {diagnosis}
            ALLERGIES: {', '.join(allergies) if allergies else 'None reported'}
            CURRENT MEDICATIONS: {', '.join(current_medications) if current_medications else 'None'}
            
            TOP RECOMMENDED TREATMENTS:
            {rec_text}
            
            Please provide:
            1. A brief explanation of why these medications are suitable for the diagnosed condition
            2. Any potential medication interactions with current medications
            3. Any lifestyle recommendations that would complement the treatment
            4. Important monitoring considerations or warning signs the patient should be aware of
            """
            
            # Make API request to KimiAI
            headers = {
                "Authorization": f"Bearer {KIMI_API_KEY}",
                "Content-Type": "application/json"
            }
            
            data = {
                "model": "anthropic/claude-3-sonnet",
                "messages": [
                    {"role": "user", "content": prompt}
                ]
            }
            
            print("Requesting AI insights...")
            response = requests.post(KIMI_API_URL, headers=headers, json=data)
            result = response.json()
            
            # Extract the response
            if 'choices' in result and len(result['choices']) > 0:
                return result['choices'][0]['message']['content']
            else:
                print(f"Unexpected API response format: {result}")
                return "AI insights not available at this time."
        except Exception as e:
            print(f"Error getting AI insights: {e}")
            return "AI insights not available at this time."

def main():
    """Main entry point for recommendation system"""
    print("\n===== EvoDoc Treatment Recommendation System =====\n")
    
    # Initialize recommendation system
    recommender = TreatmentRecommender()
    
    # Get patient information
    print("----- Patient Information -----\n")
    patient_name = input("Patient Name: ")
    
    # Get age with validation
    while True:
        try:
            age = int(input("Age: "))
            if 0 < age < 120:
                break
            print("Please enter a valid age (1-119)")
        except ValueError:
            print("Please enter a numeric age")
    
    # Get gender with validation
    while True:
        gender = input("Gender (M/F): ").upper()
        if gender in ['M', 'F']:
            break
        print("Please enter M or F")
    
    # Get symptoms
    symptoms = input("Current Symptoms (comma separated): ")
    
    # Get allergies
    allergies_input = input("Allergies (comma separated, press Enter if none): ")
    allergies = [a.strip() for a in allergies_input.split(',') if a.strip()]
    
    # Get current medications
    medications_input = input("Current Medications (comma separated, press Enter if none): ")
    medications = [m.strip() for m in medications_input.split(',') if m.strip()]
    
    # Format patient info
    patient_info = {
        "name": patient_name,
        "age": age,
        "gender": gender,
        "symptoms": symptoms,
        "allergies": allergies,
        "current_medications": medications
    }
    
    # Get recommendations
    print("\nAnalyzing and generating recommendations...")
    results = recommender.get_recommendations(patient_info)
    
    # Display results
    print("\n===== DIAGNOSIS AND TREATMENT RECOMMENDATIONS =====\n")
    print(f"DIAGNOSIS: {results['diagnosis']}\n")
    
    # Show recommendations
    print("RECOMMENDED TREATMENTS:")
    if not results['recommendations']:
        print("No safe treatment recommendations found for this patient.")
    else:
        for i, rec in enumerate(results['recommendations']):
            print(f"{i+1}. {rec['medication']} ({rec['drug_class']})")
            print(f"   Effectiveness: {rec['effectiveness']:.0%}")
            
            if rec['is_first_line']:
                print(f"   \033[1mFirst-line treatment\033[0m")
            
            if rec['interaction_warning']:
                print(f"   \033[91mWarning:\033[0m {rec['interaction_warning']}")
            
            if rec['side_effects']:
                print("   Potential side effects:")
                for se in rec['side_effects']:
                    print(f"   - {se['name']} (Severity: {se['severity']:.0%}, Frequency: {se['frequency']:.0%})")
            
            print()
    
    # Show contraindications
    if results['contraindications']:
        print("\nCONTRAINDICATED MEDICATIONS:")
        for i, contra in enumerate(results['contraindications']):
            print(f"{i+1}. {contra['medication']} ({contra['drug_class']}): {contra['reason']}")
        print()
    else:
        print("\nNo contraindicated medications identified.")
    
    # Show AI insights
    print("\n===== MEDICAL INSIGHTS =====\n")
    print(results['ai_insights'])

if __name__ == "__main__":
    main()
