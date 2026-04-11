<<<<<<< HEAD
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime

class Patient(Base):
    __tablename__ = "patients"
    
    id = Column(Integer, primary_key=True, index=True)
    nom = Column(String, index=True)
    prenom = Column(String, index=True)
    date_naissance = Column(DateTime)
    email = Column(String, unique=True, index=True)
    telephone = Column(String)
    adresse = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    dossier = relationship("Dossier", back_populates="patient", uselist=False)
    consultations = relationship("Consultation", back_populates="patient")

class Medecin(Base):
    __tablename__ = "medecins"
    
    id = Column(Integer, primary_key=True, index=True)
    nom = Column(String, index=True)
    prenom = Column(String, index=True)
    specialite = Column(String)
    email = Column(String, unique=True, index=True)
    telephone = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    consultations = relationship("Consultation", back_populates="medecin")
    prescriptions = relationship("Prescription", back_populates="medecin")

class Dossier(Base):
    __tablename__ = "dossiers"
    
    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("patients.id"), unique=True)
    antecedents = Column(Text)
    allergies = Column(Text)
    groupe_sanguin = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    patient = relationship("Patient", back_populates="dossier")

class Consultation(Base):
    __tablename__ = "consultations"
    
    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("patients.id"))
    medecin_id = Column(Integer, ForeignKey("medecins.id"))
    date_consultation = Column(DateTime, default=datetime.utcnow)
    motif = Column(String)
    diagnostic = Column(Text)
    notes = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    patient = relationship("Patient", back_populates="consultations")
    medecin = relationship("Medecin", back_populates="consultations")
    prescriptions = relationship("Prescription", back_populates="consultation")

class Medicament(Base):
    __tablename__ = "medicaments"
    
    id = Column(Integer, primary_key=True, index=True)
    nom = Column(String, index=True)
    dosage = Column(String)
    forme = Column(String)
    description = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)

class Prescription(Base):
    __tablename__ = "prescriptions"
    
    id = Column(Integer, primary_key=True, index=True)
    consultation_id = Column(Integer, ForeignKey("consultations.id"))
    medecin_id = Column(Integer, ForeignKey("medecins.id"))
    medicament_id = Column(Integer, ForeignKey("medicaments.id"))
    dosage = Column(String)
    duree = Column(String)
    instructions = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    consultation = relationship("Consultation", back_populates="prescriptions")
    medecin = relationship("Medecin", back_populates="prescriptions")
=======
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime

class Patient(Base):
    __tablename__ = "patients"
    
    id = Column(Integer, primary_key=True, index=True)
    nom = Column(String, index=True)
    prenom = Column(String, index=True)
    date_naissance = Column(DateTime)
    email = Column(String, unique=True, index=True)
    telephone = Column(String)
    adresse = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    dossier = relationship("Dossier", back_populates="patient", uselist=False)
    consultations = relationship("Consultation", back_populates="patient")

class Medecin(Base):
    __tablename__ = "medecins"
    
    id = Column(Integer, primary_key=True, index=True)
    nom = Column(String, index=True)
    prenom = Column(String, index=True)
    specialite = Column(String)
    email = Column(String, unique=True, index=True)
    telephone = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    consultations = relationship("Consultation", back_populates="medecin")
    prescriptions = relationship("Prescription", back_populates="medecin")

class Dossier(Base):
    __tablename__ = "dossiers"
    
    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("patients.id"), unique=True)
    antecedents = Column(Text)
    allergies = Column(Text)
    groupe_sanguin = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    patient = relationship("Patient", back_populates="dossier")

class Consultation(Base):
    __tablename__ = "consultations"
    
    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("patients.id"))
    medecin_id = Column(Integer, ForeignKey("medecins.id"))
    date_consultation = Column(DateTime, default=datetime.utcnow)
    motif = Column(String)
    diagnostic = Column(Text)
    notes = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    patient = relationship("Patient", back_populates="consultations")
    medecin = relationship("Medecin", back_populates="consultations")
    prescriptions = relationship("Prescription", back_populates="consultation")

class Medicament(Base):
    __tablename__ = "medicaments"
    
    id = Column(Integer, primary_key=True, index=True)
    nom = Column(String, index=True)
    dosage = Column(String)
    forme = Column(String)
    description = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)

class Prescription(Base):
    __tablename__ = "prescriptions"
    
    id = Column(Integer, primary_key=True, index=True)
    consultation_id = Column(Integer, ForeignKey("consultations.id"))
    medecin_id = Column(Integer, ForeignKey("medecins.id"))
    medicament_id = Column(Integer, ForeignKey("medicaments.id"))
    dosage = Column(String)
    duree = Column(String)
    instructions = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    consultation = relationship("Consultation", back_populates="prescriptions")
    medecin = relationship("Medecin", back_populates="prescriptions")
>>>>>>> a785b0a5c15f95b802090df3bc656f76f1fd0a44
