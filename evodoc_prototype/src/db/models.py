from sqlalchemy import Column, Integer, String, Float, ForeignKey, Table, DateTime, Text, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from .config import Base

# Association tables for many-to-many relationships
patient_allergy = Table(
    "patient_allergy",
    Base.metadata,
    Column("patient_id", Integer, ForeignKey("patients.id"), primary_key=True),
    Column("allergy_id", Integer, ForeignKey("allergies.id"), primary_key=True)
)

patient_medication = Table(
    "patient_medication",
    Base.metadata,
    Column("patient_id", Integer, ForeignKey("patients.id"), primary_key=True),
    Column("medication_id", Integer, ForeignKey("medications.id"), primary_key=True),
    Column("start_date", DateTime, default=datetime.utcnow),
    Column("end_date", DateTime, nullable=True),
    Column("dosage", String, nullable=True),
    Column("frequency", String, nullable=True)
)

medication_ingredient = Table(
    "medication_ingredient",
    Base.metadata,
    Column("medication_id", Integer, ForeignKey("medications.id"), primary_key=True),
    Column("ingredient_id", Integer, ForeignKey("ingredients.id"), primary_key=True)
)

# Patient model
class Patient(Base):
    __tablename__ = "patients"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    age = Column(Integer)
    gender = Column(String)
    medical_history = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    allergies = relationship("Allergy", secondary=patient_allergy, back_populates="patients")
    medications = relationship("Medication", secondary=patient_medication, back_populates="patients")
    appointments = relationship("Appointment", back_populates="patient")
    treatment_feedbacks = relationship("TreatmentFeedback", back_populates="patient")

# Doctor model
class Doctor(Base):
    __tablename__ = "doctors"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    specialization = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    appointments = relationship("Appointment", back_populates="doctor")
    treatments = relationship("Treatment", back_populates="doctor")

# Allergy model
class Allergy(Base):
    __tablename__ = "allergies"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, unique=True)
    description = Column(Text, nullable=True)
    
    # Relationships
    patients = relationship("Patient", secondary=patient_allergy, back_populates="allergies")
    ingredients = relationship("Ingredient", back_populates="allergies")

# Medication model
class Medication(Base):
    __tablename__ = "medications"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, unique=True)
    description = Column(Text, nullable=True)
    typical_dosage = Column(String, nullable=True)
    
    # Relationships
    patients = relationship("Patient", secondary=patient_medication, back_populates="medications")
    ingredients = relationship("Ingredient", secondary=medication_ingredient, back_populates="medications")
    treatments = relationship("Treatment", back_populates="medication")
    side_effects = relationship("SideEffect", back_populates="medication")

# Ingredient model (for medication components)
class Ingredient(Base):
    __tablename__ = "ingredients"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, unique=True)
    description = Column(Text, nullable=True)
    
    # Relationships
    medications = relationship("Medication", secondary=medication_ingredient, back_populates="ingredients")
    allergies = relationship("Allergy", back_populates="ingredients")

# Appointment model
class Appointment(Base):
    __tablename__ = "appointments"

    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("patients.id"))
    doctor_id = Column(Integer, ForeignKey("doctors.id"))
    date = Column(DateTime)
    symptoms = Column(Text)
    status = Column(String)  # pending, completed, cancelled
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    patient = relationship("Patient", back_populates="appointments")
    doctor = relationship("Doctor", back_populates="appointments")
    treatments = relationship("Treatment", back_populates="appointment")

# Treatment model
class Treatment(Base):
    __tablename__ = "treatments"

    id = Column(Integer, primary_key=True, index=True)
    appointment_id = Column(Integer, ForeignKey("appointments.id"))
    doctor_id = Column(Integer, ForeignKey("doctors.id"))
    medication_id = Column(Integer, ForeignKey("medications.id"))
    dosage = Column(String)
    frequency = Column(String)
    instructions = Column(Text, nullable=True)
    start_date = Column(DateTime, default=datetime.utcnow)
    end_date = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    appointment = relationship("Appointment", back_populates="treatments")
    doctor = relationship("Doctor", back_populates="treatments")
    medication = relationship("Medication", back_populates="treatments")
    feedbacks = relationship("TreatmentFeedback", back_populates="treatment")

# Treatment Feedback model
class TreatmentFeedback(Base):
    __tablename__ = "treatment_feedbacks"

    id = Column(Integer, primary_key=True, index=True)
    treatment_id = Column(Integer, ForeignKey("treatments.id"))
    patient_id = Column(Integer, ForeignKey("patients.id"))
    effectiveness = Column(Integer)  # Rating 1-10
    side_effects = Column(Text, nullable=True)
    comments = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    treatment = relationship("Treatment", back_populates="feedbacks")
    patient = relationship("Patient", back_populates="treatment_feedbacks")

# Side Effect model
class SideEffect(Base):
    __tablename__ = "side_effects"

    id = Column(Integer, primary_key=True, index=True)
    medication_id = Column(Integer, ForeignKey("medications.id"))
    name = Column(String)
    description = Column(Text, nullable=True)
    frequency = Column(Float)  # Probability of occurrence
    severity = Column(Integer)  # Scale 1-10
    
    # Relationships
    medication = relationship("Medication", back_populates="side_effects")
