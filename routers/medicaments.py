from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

import models
import schemas
from database import get_db

router = APIRouter(prefix="/medicaments", tags=["Médicaments"])

@router.get("/", response_model=List[schemas.MedOut])
def lister_medicaments(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Lister tous les médicaments enregistrés dans la base.
    """
    medicaments = db.query(models.Medicament).offset(skip).limit(limit).all()
    return medicaments

@router.post("/", response_model=schemas.MedOut)
def ajouter_medicament(medicament: schemas.MedCreate, db: Session = Depends(get_db)):
    """
    Ajouter un nouveau médicament dans la base de données.
    """
    db_medicament = models.Medicament(**medicament.model_dump() if hasattr(medicament, 'model_dump') else medicament.dict())
    db.add(db_medicament)
    db.commit()
    db.refresh(db_medicament)
    return db_medicament
