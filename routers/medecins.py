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

# Kreyasyon yon router pou gwoupe tout wout ki gen rapò ak doktè yo (Médecins)
router = APIRouter(prefix="/medecins", tags=["Médecins"])

# ---------------------------------------------------------------------
# Wout (GET): Pou lister tout doktè ki anrejistre yo
# ---------------------------------------------------------------------
@router.get("/")
def lister_medecins(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    # Fè yon rechèch nan baz done a pou pran lis doktè yo ak yon ti limit (pagination)
    return db.query(models.Medecin).offset(skip).limit(limit).all()

# ---------------------------------------------------------------------
# Wout (GET): Pou jwenn tout konsiltasyon yon doktè espesifik (One-to-Many)
# ---------------------------------------------------------------------
@router.get("/{id}/consultations")
def consultations_medecin(id: int, db: Session = Depends(get_db)):
    # 1. Verifye si doktè a egziste vre nan baz done a
    medecin = db.query(models.Medecin).filter(models.Medecin.id == id).first()
    if not medecin:
        # Si nou pa jwenn li, voye yon erè 404 (Not Found) ba itilizatè a
        raise HTTPException(status_code=404, detail="Médecin non trouvé")
    
    # 2. Si doktè a la, chache tout konsiltasyon ki gen medecin_id ki koresponn a id sa a
    consultations = db.query(models.Consultation).filter(models.Consultation.medecin_id == id).all()
    return consultations

# ---------------------------------------------------------------------
# Wout (POST): Pou kreye yon nouvo doktè
# ---------------------------------------------------------------------
@router.post("/")
def creer_medecin(medecin: schemas.MedecinCreate, db: Session = Depends(get_db)):
    # 1. Konvèti done klyan an (Pydantic) an fòma baz done a (SQLAlchemy)
    db_medecin = models.Medecin(**medecin.dict())
    
    # 2. Prepare li nan sesyon an epi sove chanjman an (commit)
    db.add(db_medecin)
    db.commit()
    
    # 3. Rafrechi done yo pou nou pran id inik ki fenk jenere a
    db.refresh(db_medecin)
    return db_medecin

# ---------------------------------------------------------------------
# Wout (PUT): Pou modifye done yon doktè ki la deja
# ---------------------------------------------------------------------
@router.put("/{id}")
def modifier_medecin(id: int, medecin_data: schemas.MedecinCreate, db: Session = Depends(get_db)):
    # 1. Jwenn doktè konsène an
    db_medecin = db.query(models.Medecin).filter(models.Medecin.id == id).first()
    if not db_medecin:
        raise HTTPException(status_code=404, detail="Médecin non trouvé")
    
    # 2. Mete ajou atribi yo ak valè nouvo yo
    for key, value in medecin_data.dict().items():
        setattr(db_medecin, key, value)
        
    # 3. Akspete chanjman yo andedan SQLite la
    db.commit()
    db.refresh(db_medecin)
    return db_medecin

# ---------------------------------------------------------------------
# Wout (DELETE): Pou efase konplètman yon doktè nan baz la
# ---------------------------------------------------------------------
@router.delete("/{id}")
def supprimer_medecin(id: int, db: Session = Depends(get_db)):
    # 1. Rechèch e verifye
    db_medecin = db.query(models.Medecin).filter(models.Medecin.id == id).first()
    if not db_medecin:
        raise HTTPException(status_code=404, detail="Médecin non trouvé")
        
    # 2. Fonksyon delete epi sove jèfò a ak commit
    db.delete(db_medecin)
    db.commit()
    return {"message": "Médecin supprimé"}
