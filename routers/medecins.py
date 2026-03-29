from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

import models
import schemas
from database import get_db

router = APIRouter(prefix="/medecins", tags=["Médecins"])

@router.get("/")
def lister_medecins(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(models.Medecin).offset(skip).limit(limit).all()

@router.get("/{id}/consultations")
def consultations_medecin(id: int, db: Session = Depends(get_db)):
    medecin = db.query(models.Medecin).filter(models.Medecin.id == id).first()
    if not medecin:
        raise HTTPException(status_code=404, detail="Médecin non trouvé")
    consultations = db.query(models.Consultation).filter(models.Consultation.medecin_id == id).all()
    return consultations

@router.post("/")
def creer_medecin(medecin: schemas.MedecinCreate, db: Session = Depends(get_db)):
    db_medecin = models.Medecin(**medecin.dict())
    db.add(db_medecin)
    db.commit()
    db.refresh(db_medecin)
    return db_medecin

@router.put("/{id}")
def modifier_medecin(id: int, medecin_data: schemas.MedecinCreate, db: Session = Depends(get_db)):
    db_medecin = db.query(models.Medecin).filter(models.Medecin.id == id).first()
    if not db_medecin:
        raise HTTPException(status_code=404, detail="Médecin non trouvé")
    for key, value in medecin_data.dict().items():
        setattr(db_medecin, key, value)
    db.commit()
    db.refresh(db_medecin)
    return db_medecin

@router.delete("/{id}")
def supprimer_medecin(id: int, db: Session = Depends(get_db)):
    db_medecin = db.query(models.Medecin).filter(models.Medecin.id == id).first()
    if not db_medecin:
        raise HTTPException(status_code=404, detail="Médecin non trouvé")
    db.delete(db_medecin)
    db.commit()
    return {"message": "Médecin supprimé"}
