from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List, Optional
from pydantic import BaseModel

from ..db.config import get_db
from ..db.models import Patient, Doctor, Appointment, Treatment, Allergy
from ..ml.predict import recommend_treatments

# Create FastAPI app
app = FastAPI(
    title="EvoDoc API",
    description="API for EvoDoc medical treatment recommendation system",
    version="0.1.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5000", "http://localhost:5001"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models for request/response
class PatientCreate(BaseModel):
    name: str
    age: int
    gender: str
    medical_history: Optional[str] = None

class PatientResponse(BaseModel):
    id: int
    name: str
    age: int
    gender: str
    medical_history: Optional[str] = None
    
    class Config:
        orm_mode = True

class AppointmentCreate(BaseModel):
    patient_id: int
    doctor_id: int
    date: str
    symptoms: str

class AppointmentResponse(BaseModel):
    id: int
    patient_id: int
    doctor_id: int
    patient_name: str
    doctor_name: str
    date: str
    symptoms: str
    status: str
    
    class Config:
        orm_mode = True

class TreatmentCreate(BaseModel):
    appointment_id: int
    doctor_id: int
    medication_id: int
    dosage: str
    frequency: str
    instructions: Optional[str] = None

class TreatmentResponse(BaseModel):
    id: int
    appointment_id: int
    medication_name: str
    dosage: str
    frequency: str
    instructions: Optional[str] = None
    
    class Config:
        orm_mode = True

class RecommendationRequest(BaseModel):
    patient_id: int
    symptoms: str
    current_medications: Optional[List[str]] = None

class MedicationRecommendation(BaseModel):
    medication: str
    medication_id: int
    effectiveness: float
    confidence: float
    side_effects: Optional[List[dict]] = None

class Contraindication(BaseModel):
    medication: str
    ingredient: str
    reason: str

class Alternative(BaseModel):
    original: str
    alternative: str
    reason: str

class RecommendationResponse(BaseModel):
    recommendations: List[MedicationRecommendation]
    contraindications: List[Contraindication]
    alternatives: List[Alternative]
    explanation: str

@app.get("/")
def read_root():
    return {"message": "Welcome to EvoDoc API"}

@app.post("/patients/", response_model=PatientResponse)
def create_patient(patient: PatientCreate, db: Session = Depends(get_db)):
    db_patient = Patient(
        name=patient.name,
        age=patient.age,
        gender=patient.gender,
        medical_history=patient.medical_history
    )
    db.add(db_patient)
    db.commit()
    db.refresh(db_patient)
    return db_patient

@app.get("/patients/", response_model=List[PatientResponse])
def read_patients(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    patients = db.query(Patient).offset(skip).limit(limit).all()
    return patients

@app.get("/patients/{patient_id}", response_model=PatientResponse)
def read_patient(patient_id: int, db: Session = Depends(get_db)):
    patient = db.query(Patient).filter(Patient.id == patient_id).first()
    if patient is None:
        raise HTTPException(status_code=404, detail="Patient not found")
    return patient

@app.post("/appointments/", response_model=AppointmentResponse)
def create_appointment(appointment: AppointmentCreate, db: Session = Depends(get_db)):
    # Verify patient and doctor exist
    patient = db.query(Patient).filter(Patient.id == appointment.patient_id).first()
    doctor = db.query(Doctor).filter(Doctor.id == appointment.doctor_id).first()
    
    if patient is None:
        raise HTTPException(status_code=404, detail="Patient not found")
    if doctor is None:
        raise HTTPException(status_code=404, detail="Doctor not found")
    
    db_appointment = Appointment(
        patient_id=appointment.patient_id,
        doctor_id=appointment.doctor_id,
        date=appointment.date,
        symptoms=appointment.symptoms,
        status="pending"
    )
    db.add(db_appointment)
    db.commit()
    db.refresh(db_appointment)
    
    # Return with names
    return {
        "id": db_appointment.id,
        "patient_id": db_appointment.patient_id,
        "doctor_id": db_appointment.doctor_id,
        "patient_name": patient.name,
        "doctor_name": doctor.name,
        "date": db_appointment.date,
        "symptoms": db_appointment.symptoms,
        "status": db_appointment.status
    }

@app.get("/appointments/", response_model=List[AppointmentResponse])
def read_appointments(skip: int = 0, limit: int = 100, doctor_id: Optional[int] = None, 
                     patient_id: Optional[int] = None, db: Session = Depends(get_db)):
    query = db.query(
        Appointment, 
        Patient.name.label("patient_name"), 
        Doctor.name.label("doctor_name")
    ).join(
        Patient, Appointment.patient_id == Patient.id
    ).join(
        Doctor, Appointment.doctor_id == Doctor.id
    )
    
    # Filter by doctor or patient if provided
    if doctor_id:
        query = query.filter(Appointment.doctor_id == doctor_id)
    if patient_id:
        query = query.filter(Appointment.patient_id == patient_id)
    
    appointments = query.offset(skip).limit(limit).all()
    
    # Format response
    result = []
    for appt, patient_name, doctor_name in appointments:
        result.append({
            "id": appt.id,
            "patient_id": appt.patient_id,
            "doctor_id": appt.doctor_id,
            "patient_name": patient_name,
            "doctor_name": doctor_name,
            "date": appt.date,
            "symptoms": appt.symptoms,
            "status": appt.status
        })
    
    return result

@app.get("/appointments/{appointment_id}", response_model=AppointmentResponse)
def read_appointment(appointment_id: int, db: Session = Depends(get_db)):
    appointment = db.query(
        Appointment, 
        Patient.name.label("patient_name"), 
        Doctor.name.label("doctor_name")
    ).join(
        Patient, Appointment.patient_id == Patient.id
    ).join(
        Doctor, Appointment.doctor_id == Doctor.id
    ).filter(
        Appointment.id == appointment_id
    ).first()
    
    if appointment is None:
        raise HTTPException(status_code=404, detail="Appointment not found")
    
    appt, patient_name, doctor_name = appointment
    
    return {
        "id": appt.id,
        "patient_id": appt.patient_id,
        "doctor_id": appt.doctor_id,
        "patient_name": patient_name,
        "doctor_name": doctor_name,
        "date": appt.date,
        "symptoms": appt.symptoms,
        "status": appt.status
    }

@app.post("/treatments/", response_model=TreatmentResponse)
def create_treatment(treatment: TreatmentCreate, db: Session = Depends(get_db)):
    from sqlalchemy import text
    
    # Get medication name (direct query for simplicity)
    result = db.execute(
        text("SELECT name FROM medications WHERE id = :med_id"),
        {"med_id": treatment.medication_id}
    ).fetchone()
    
    if result is None:
        raise HTTPException(status_code=404, detail="Medication not found")
    
    medication_name = result[0]
    
    db_treatment = Treatment(
        appointment_id=treatment.appointment_id,
        doctor_id=treatment.doctor_id,
        medication_id=treatment.medication_id,
        dosage=treatment.dosage,
        frequency=treatment.frequency,
        instructions=treatment.instructions
    )
    db.add(db_treatment)
    db.commit()
    db.refresh(db_treatment)
    
    # Return with medication name
    return {
        "id": db_treatment.id,
        "appointment_id": db_treatment.appointment_id,
        "medication_name": medication_name,
        "dosage": db_treatment.dosage,
        "frequency": db_treatment.frequency,
        "instructions": db_treatment.instructions
    }

@app.post("/recommend/", response_model=RecommendationResponse)
def get_recommendations(req: RecommendationRequest, db: Session = Depends(get_db)):
    # Get patient data
    patient = db.query(Patient).filter(Patient.id == req.patient_id).first()
    if patient is None:
        raise HTTPException(status_code=404, detail="Patient not found")
    
    # Get patient allergies
    patient_allergies = db.query(
        Allergy.id
    ).join(
        "patients"
    ).filter(
        Patient.id == req.patient_id
    ).all()
    
    allergy_ids = [allergy[0] for allergy in patient_allergies]
    
    # Prepare patient data for ML model
    patient_data = {
        "age": patient.age,
        "gender": patient.gender,
        "diagnosis": req.symptoms,
        "medications": req.current_medications or []
    }
    
    # Get recommendations
    recommendations = recommend_treatments(patient_data, allergy_ids)
    
    return recommendations

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
