from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

import models
import schemas
from database import get_db

router = APIRouter(prefix="/consultations", tags=["Consultations"])

@router.get("/")
def lister_consultations(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(models.Consultation).offset(skip).limit(limit).all()

@router.get("/{id}")
def obtenir_consultation(id: int, db: Session = Depends(get_db)):
    consultation = db.query(models.Consultation).filter(models.Consultation.id == id).first()
    if not consultation:
        raise HTTPException(status_code=404, detail="Consultation non trouvée")
    return consultation

@router.post("/")
def creer_consultation(consultation: schemas.ConsultCreate, db: Session = Depends(get_db)):
    patient = db.query(models.Patient).filter(models.Patient.id == consultation.patient_id).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Patient non trouvé")
    medecin = db.query(models.Medecin).filter(models.Medecin.id == consultation.medecin_id).first()
    if not medecin:
        raise HTTPException(status_code=404, detail="Médecin non trouvé")
        
    db_consultation = models.Consultation(**consultation.dict())
    db.add(db_consultation)
    db.commit()
    db.refresh(db_consultation)
    return db_consultation

@router.delete("/{id}")
def supprimer_consultation(id: int, db: Session = Depends(get_db)):
    consultation = db.query(models.Consultation).filter(models.Consultation.id == id).first()
    if not consultation:
        raise HTTPException(status_code=404, detail="Consultation non trouvée")
    db.delete(consultation)
    db.commit()
    return {"message": "Consultation supprimée"}
