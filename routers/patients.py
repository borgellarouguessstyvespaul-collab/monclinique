# =====================================================================
# Module (Routers) développé et géré par : Styves Paul Borgella
# Projet : API REST Clinique Médicale - Groupe C
# =====================================================================
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

import models
import schemas
from database import get_db

# Router k ap gwoupe wout pou patients
router = APIRouter(prefix="/patients", tags=["Patients"])

# ---------------------------------------------------------------------
# Wout (GET): Pou afiche tout pasyan klinik la
# ---------------------------------------------------------------------
@router.get("/")
def lister_patients(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    # Demann de baz SQLAlchemy a k ap rale done yo
    return db.query(models.Patient).offset(skip).limit(limit).all()

# ---------------------------------------------------------------------
# Wout (GET): Jwenn yon sèl pasyan (ak tout dosye medikal li, One-to-One)
# ---------------------------------------------------------------------
@router.get("/{id}")
def obtenir_patient(id: int, db: Session = Depends(get_db)):
    # Evalye si id pasyan an egziste
    db_patient = db.query(models.Patient).filter(models.Patient.id == id).first()
    if not db_patient:
        raise HTTPException(status_code=404, detail="Patient non trouvé")
    
    # Retounen done a apèl Pydantic Schema a
    return db_patient

# ---------------------------------------------------------------------
# Wout (GET): Rale konsiltasyon pou Yon Sèl pasyan (One-to-Many)
# ---------------------------------------------------------------------
@router.get("/{id}/consultations")
def consultations_patient(id: int, db: Session = Depends(get_db)):
    # 1. Double verifye validite pasyan id a
    db_patient = db.query(models.Patient).filter(models.Patient.id == id).first()
    if not db_patient:
        raise HTTPException(status_code=404, detail="Patient non trouvé")
        
    # 2. Pran tout randevou/konsiltasyon kote pasyan ID li ye
    consultations = db.query(models.Consultation).filter(models.Consultation.patient_id == id).all()
    return consultations

# ---------------------------------------------------------------------
# Wout (POST): Anregistrer yon nouvo pasyan
# ---------------------------------------------------------------------
@router.post("/")
def creer_patient(patient: schemas.PatientCreate, db: Session = Depends(get_db)):
    # Transforme done yo an objè pou entegrasyon DB
    db_patient = models.Patient(**patient.dict())
    
    # Sove kreyasyon an
    db.add(db_patient)
    db.commit()
    db.refresh(db_patient)
    return db_patient

# ---------------------------------------------------------------------
# Wout (PUT): Mete enfòmasyon pasyan an à jou
# ---------------------------------------------------------------------
@router.put("/{id}")
def modifier_patient(id: int, patient_data: schemas.PatientCreate, db: Session = Depends(get_db)):
    # 1. Rale pasyan a w vle edite a
    db_patient = db.query(models.Patient).filter(models.Patient.id == id).first()
    if not db_patient:
        raise HTTPException(status_code=404, detail="Patient non trouvé")
        
    # 2. Rekolte done sou paramèt yo e mete yo a jou
    for key, value in patient_data.dict().items():
        setattr(db_patient, key, value)
        
    # 3. Kontwòle transfè chanjman yo anndan DB an
    db.commit()
    db.refresh(db_patient)
    return db_patient

# ---------------------------------------------------------------------
# Wout (DELETE): Efase yon pasyan
# ---------------------------------------------------------------------
@router.delete("/{id}")
def supprimer_patient(id: int, db: Session = Depends(get_db)):
    # Jwenn pasyan an 
    db_patient = db.query(models.Patient).filter(models.Patient.id == id).first()
    if not db_patient:
        raise HTTPException(status_code=404, detail="Patient non trouvé")
        
    # Siprime l nan baz la.
    db.delete(db_patient)
    db.commit()
    return {"message": "Patient supprimé avec succès"}
