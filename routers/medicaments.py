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

# Router pou jesyon famasi / medikaman ki disponib
router = APIRouter(prefix="/medicaments", tags=["Médicaments"])

# ---------------------------------------------------------------------
# Wout (GET): Bay lis tout medikaman nan klinik la
# ---------------------------------------------------------------------
@router.get("/")
def lister_medicaments(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    # Rale done yo ak pagination
    medicaments = db.query(models.Medicament).offset(skip).limit(limit).all()
    return medicaments

# ---------------------------------------------------------------------
# Wout (POST): Antre yon pwodwi / medikaman nèf nan baz la
# ---------------------------------------------------------------------
@router.post("/")
def ajouter_medicament(medicament: schemas.MedCreate, db: Session = Depends(get_db)):
    # Kreye medikaman an nan fòma SQLAlchemy (après validation Pydantic Schema MedCreate)
    db_medicament = models.Medicament(**medicament.dict())
    
    # Push l nan SQLite SQLite
    db.add(db_medicament)
    db.commit()
    db.refresh(db_medicament)
    return db_medicament
