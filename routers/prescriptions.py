from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

import models
import schemas
from database import get_db

router = APIRouter(prefix="/prescriptions", tags=["Prescriptions"])

@router.post("/")
def prescrire_medicament(prescription: schemas.PrescriptionCreate, db: Session = Depends(get_db)):
    consultation = db.query(models.Consultation).filter(models.Consultation.id == prescription.consultation_id).first()
    if not consultation:
        raise HTTPException(status_code=404, detail="Consultation non trouvée")
        
    medicament = db.query(models.Medicament).filter(models.Medicament.id == prescription.medicament_id).first()
    if not medicament:
        raise HTTPException(status_code=404, detail="Médicament non trouvé")
        
    if medicament in consultation.medicaments:
        raise HTTPException(status_code=400, detail="Mdicament déjà prescrit à cette consultation")
        
    consultation.medicaments.append(medicament)
    db.commit()
    return {"message": "Médicament prescrit avec succès"}

@router.delete("/{cid}/{mid}")
def retirer_medicament_prescrit(cid: int, mid: int, db: Session = Depends(get_db)):
    consultation = db.query(models.Consultation).filter(models.Consultation.id == cid).first()
    if not consultation:
        raise HTTPException(status_code=404, detail="Consultation non trouvée")
        
    medicament = db.query(models.Medicament).filter(models.Medicament.id == mid).first()
    if not medicament:
        raise HTTPException(status_code=404, detail="Médicament non trouvé")
        
    if medicament not in consultation.medicaments:
        raise HTTPException(status_code=400, detail="Médicament non associé à cette consultation")
        
    consultation.medicaments.remove(medicament)
    db.commit()
    return {"message": "Prescription retirée avec succès"}
