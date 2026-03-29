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

# Router espèsyal pou dossiers médikaux (One-to-One ak Patient)
router = APIRouter(prefix="/dossiers", tags=["Dossiers Médicaux"])

# ---------------------------------------------------------------------
# Wout (POST): Kreye yon nouvo dosye medikal pou pasyan an
# ---------------------------------------------------------------------
@router.post("/")
def creer_dossier(dossier: schemas.DossierCreate, db: Session = Depends(get_db)):
    # 1. Tcheke avèk presizyon si pasyan an egziste
    db_patient = db.query(models.Patient).filter(models.Patient.id == dossier.patient_id).first()
    if not db_patient:
        raise HTTPException(status_code=404, detail="Patient non trouvé")
    
    # 2. Relasyon One-To-One lan la: Ou paka gen de dosye anmenntan, nou tcheke sa!
    db_dossier = db.query(models.DossierMedical).filter(models.DossierMedical.patient_id == dossier.patient_id).first()
    if db_dossier:
        # Piske li geyen l deja, n ap voye yon erè 400 Bad request.
        raise HTTPException(status_code=400, detail="Ce patient a déjà un dossier médical")
        
    # 3. Kreye e anrejistre le fichier nan tab la
    nouveau_dossier = models.DossierMedical(**dossier.dict())
    db.add(nouveau_dossier)
    db.commit()
    db.refresh(nouveau_dossier)
    return nouveau_dossier

# ---------------------------------------------------------------------
# Wout (PUT): Modifye dosye medikal yon pasyan
# ---------------------------------------------------------------------
@router.put("/{patient_id}")
def modifier_dossier(patient_id: int, dossier_data: schemas.DossierCreate, db: Session = Depends(get_db)):
    # 1. Rale l pa patient_id (kòm relasyon an se One-to-one)
    db_dossier = db.query(models.DossierMedical).filter(models.DossierMedical.patient_id == patient_id).first()
    if not db_dossier:
        raise HTTPException(status_code=404, detail="Dossier médical non trouvé")
        
    # 2. Modifikasyon enfomasyon (allergies, gwoup san elatriye)
    for key, value in dossier_data.dict().items():
        # Nou p ap kite yo modifye mèt dosye a (patient_id a)
        if key != 'patient_id':
            setattr(db_dossier, key, value)
            
    # 3. Pouse chanjman yo andedan disk la
    db.commit()
    db.refresh(db_dossier)
    return db_dossier
