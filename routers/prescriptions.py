# =====================================================================
# Module (Routers) développé et géré par : Styves Paul Borgella
# Projet : API REST Clinique Médicale - Groupe C
# =====================================================================
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

import models
import schemas
from database import get_db

# Router ascosyayon (Many-to-Many connection)
router = APIRouter(prefix="/prescriptions", tags=["Prescriptions"])

# ---------------------------------------------------------------------
# Wout (POST): Ekri yon preskripsyon (Mete yon Medikaman nan yon Konsiltasyon)
# ---------------------------------------------------------------------
@router.post("/")
def prescrire_medicament(prescription: schemas.PrescriptionCreate, db: Session = Depends(get_db)):
    # 1. Validasyon : Verifye tab konsiltasyon an
    consultation = db.query(models.Consultation).filter(models.Consultation.id == prescription.consultation_id).first()
    if not consultation:
        raise HTTPException(status_code=404, detail="Consultation non trouvée")
        
    # 2. Validasyon : Verifye tab Medikaman an
    medicament = db.query(models.Medicament).filter(models.Medicament.id == prescription.medicament_id).first()
    if not medicament:
        raise HTTPException(status_code=404, detail="Médicament non trouvé")
        
    # 3. Double-chek (Many to Many): Anpeche ba l menm medikaman an de (2) fwa
    if medicament in consultation.medicaments:
        # Voye error code HTTP 400 - Bad Request
        raise HTTPException(status_code=400, detail="Ce médicament est déjà prescrit pour cette consultation")
        
    # 4. Magik Many-to-Many SQLAlchemy an! Ansèsyon andedan table pivot la fèt poukont li ak senp ".append()"
    consultation.medicaments.append(medicament)
    db.commit()
    return {"message": "Médicament prescrit avec succès"}

# ---------------------------------------------------------------------
# Wout (DELETE): Rache yon medikaman nan yon preskripsyon
# CID = consultation ID ; MID = medicament ID
# ---------------------------------------------------------------------
@router.delete("/{cid}/{mid}")
def retirer_medicament_prescrit(cid: int, mid: int, db: Session = Depends(get_db)):
    # 1. Tcheke validite konsiltasyon an
    consultation = db.query(models.Consultation).filter(models.Consultation.id == cid).first()
    if not consultation:
        raise HTTPException(status_code=404, detail="Consultation non trouvée")
        
    # 2. Asire nou id medikaman an egziste vre
    medicament = db.query(models.Medicament).filter(models.Medicament.id == mid).first()
    if not medicament:
        raise HTTPException(status_code=404, detail="Médicament non trouvé")
        
    # 3. Verifye si yo te reyèlman associe anvan nou deletel la
    if medicament not in consultation.medicaments:
        raise HTTPException(status_code=400, detail="Médicament non associé à cette consultation")
        
    # 4. SQLAlchemy ap wete l nan lis la epi l'ajiste table pivot pou kont li
    consultation.medicaments.remove(medicament)
    db.commit()
    return {"message": "Prescription retirée avec succès"}
