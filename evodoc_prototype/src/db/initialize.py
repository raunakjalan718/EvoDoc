from .config import engine, SessionLocal, Base
from .models import Patient, Doctor, Allergy, Medication, Ingredient, Appointment
from sqlalchemy.orm import Session

def create_tables():
    Base.metadata.create_all(bind=engine)

def initialize_sample_data():
    db = SessionLocal()
    
    # Check if data already exists
    if db.query(Patient).first():
        db.close()
        return
    
    # Create sample patients
    patients = [
        Patient(name="Akshit Ohri", age=28, gender="Male", medical_history="Asthma, Seasonal allergies"),
        Patient(name="Raunak Jalan", age=35, gender="Male", medical_history="Hypertension, Type 2 diabetes"),
        Patient(name="Radhika Jalan", age=30, gender="Female", medical_history="Migraine, Iron deficiency")
    ]
    db.add_all(patients)
    
    # Create sample doctor
    doctor = Doctor(name="Dr. Sarah Patel", specialization="General Medicine")
    db.add(doctor)
    
    # Create sample allergies
    allergies = [
        Allergy(name="Penicillin"),
        Allergy(name="Sulfa drugs"),
        Allergy(name="Aspirin"),
        Allergy(name="Shellfish"),
        Allergy(name="Latex"),
        Allergy(name="Ibuprofen")
    ]
    db.add_all(allergies)
    
    # Commit to get IDs
    db.commit()
    
    # Associate allergies with patients
    patients[0].allergies.extend([allergies[0], allergies[1]])  # Akshit: Penicillin, Sulfa drugs
    patients[1].allergies.extend([allergies[2], allergies[3]])  # Raunak: Aspirin, Shellfish
    patients[2].allergies.extend([allergies[4], allergies[5]])  # Radhika: Latex, Ibuprofen
    
    db.commit()
    db.close()

def main():
    create_tables()
    initialize_sample_data()
    print("Database initialized successfully!")

if __name__ == "__main__":
    main()
