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

# Router okipe rankont doktor pasyan yo
router = APIRouter(prefix="/consultations", tags=["Consultations"])

# ---------------------------------------------------------------------
# Wout (GET): Rale souple tout randevou konsultasyon
# ---------------------------------------------------------------------
@router.get("/")
def lister_consultations(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    # Jwenn list la avèk limitasyon (100 pa defo)
    return db.query(models.Consultation).offset(skip).limit(limit).all()

# ---------------------------------------------------------------------
# Wout (GET): Bay tout detay yon sèl konsiltasyon ansanm ak lès medikaman li yo
# ---------------------------------------------------------------------
@router.get("/{id}")
def obtenir_consultation(id: int, db: Session = Depends(get_db)):
    # Chache nan baz la selon ID a
    consultation = db.query(models.Consultation).filter(models.Consultation.id == id).first()
    
    # 404 pou verifye
    if not consultation:
        raise HTTPException(status_code=404, detail="Consultation non trouvée")
        
    # Schema SQLAlchemy/Pydantic la ap ranje pati medikaman yo (Many To Many) pou kont li
    return consultation

# ---------------------------------------------------------------------
# Wout (POST): Pwograme / kreye yon nouvo konsiltasyon
# ---------------------------------------------------------------------
@router.post("/")
def creer_consultation(consultation: schemas.ConsultCreate, db: Session = Depends(get_db)):
    # 1. Validation FK1: eske pasyan an la vre?
    patient = db.query(models.Patient).filter(models.Patient.id == consultation.patient_id).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Patient non trouvé")
        
    # 2. Validation FK2: eske Doktè a la vre?
    medecin = db.query(models.Medecin).filter(models.Medecin.id == consultation.medecin_id).first()
    if not medecin:
        raise HTTPException(status_code=404, detail="Médecin non trouvé")
        
    # 3. Kreyasyon e anrejistreman rankont la
    db_consultation = models.Consultation(**consultation.dict())
    db.add(db_consultation)
    db.commit()
    db.refresh(db_consultation)
    return db_consultation

# ---------------------------------------------------------------------
# Wout (DELETE): Annile konsiltasyon an nèt
# ---------------------------------------------------------------------
@router.delete("/{id}")
def supprimer_consultation(id: int, db: Session = Depends(get_db)):
    # 1. Rale konsiltasyon w vle wete a
    consultation = db.query(models.Consultation).filter(models.Consultation.id == id).first()
    if not consultation:
        raise HTTPException(status_code=404, detail="Consultation non trouvée")
        
    # 2. Sipresyon
    db.delete(consultation)
    db.commit()
    return {"message": "Consultation supprimée avec succès"}
