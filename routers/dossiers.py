from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

import models
import schemas
from database import get_db

router = APIRouter(prefix="/dossiers", tags=["Dossiers Médicaux"])

@router.post("/")
def creer_dossier(dossier: schemas.DossierCreate, db: Session = Depends(get_db)):
    db_patient = db.query(models.Patient).filter(models.Patient.id == dossier.patient_id).first()
    if not db_patient:
        raise HTTPException(status_code=404, detail="Patient non trouvé")
    
    db_dossier = db.query(models.DossierMedical).filter(models.DossierMedical.patient_id == dossier.patient_id).first()
    if db_dossier:
        raise HTTPException(status_code=400, detail="Ce patient a déjà un dossier médical")
        
    nouveau_dossier = models.DossierMedical(**dossier.dict())
    db.add(nouveau_dossier)
    db.commit()
    db.refresh(nouveau_dossier)
    return nouveau_dossier

@router.put("/{patient_id}")
def modifier_dossier(patient_id: int, dossier_data: schemas.DossierCreate, db: Session = Depends(get_db)):
    db_dossier = db.query(models.DossierMedical).filter(models.DossierMedical.patient_id == patient_id).first()
    if not db_dossier:
        raise HTTPException(status_code=404, detail="Dossier médical non trouvé")
    for key, value in dossier_data.dict().items():
        if key != 'patient_id':  # On ne modifie pas la clé One-to-One
            setattr(db_dossier, key, value)
    db.commit()
    db.refresh(db_dossier)
    return db_dossier
