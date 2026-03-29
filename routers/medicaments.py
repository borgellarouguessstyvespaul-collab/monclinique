from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

import models
import schemas
from database import get_db

router = APIRouter(prefix="/medicaments", tags=["Médicaments"])

@router.get("/")
def lister_medicaments(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    medicaments = db.query(models.Medicament).offset(skip).limit(limit).all()
    return medicaments

@router.post("/")
def ajouter_medicament(medicament: schemas.MedCreate, db: Session = Depends(get_db)):
    db_medicament = models.Medicament(**medicament.dict())
    db.add(db_medicament)
    db.commit()
    db.refresh(db_medicament)
    return db_medicament
