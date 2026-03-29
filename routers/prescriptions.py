from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

import models
import schemas
from database import get_db

router = APIRouter(prefix="/prescriptions", tags=["Prescriptions"])

@router.post("/")
def prescrire_medicament(prescription: schemas.PrescriptionCreate, db: Session = Depends(get_db)):
    """
    Prescrire un médicament à une consultation (Many-to-Many).
    On suppose ici que schemas.PrescriptionCreate contient:
      - consultation_id
      - medicament_id
    Et que models.Consultation possède la relationship 'medicaments'.
    """
    # Vérifier que la consultation existe
    consultation = db.query(models.Consultation).filter(models.Consultation.id == prescription.consultation_id).first()
    if not consultation:
        raise HTTPException(status_code=404, detail="Consultation non trouvée")
        
    # Vérifier que le médicament existe
    medicament = db.query(models.Medicament).filter(models.Medicament.id == prescription.medicament_id).first()
    if not medicament:
        raise HTTPException(status_code=404, detail="Médicament non trouvé")
        
    # Optionnel : vérifier si déjà prescrit
    if medicament in consultation.medicaments:
        raise HTTPException(status_code=400, detail="Ce médicament est déjà prescrit pour cette consultation")
        
    # Ajouter le médicament via la relation ORM
    consultation.medicaments.append(medicament)
    db.commit()
    
    return {"message": "Médicament prescrit avec succès"}

@router.delete("/{cid}/{mid}")
def retirer_medicament_prescrit(cid: int, mid: int, db: Session = Depends(get_db)):
    """
    Retirer un médicament prescrit d'une consultation.
    """
    # Vérifier que la consultation existe
    consultation = db.query(models.Consultation).filter(models.Consultation.id == cid).first()
    if not consultation:
        raise HTTPException(status_code=404, detail="Consultation non trouvée")
        
    # Vérifier que le médicament existe
    medicament = db.query(models.Medicament).filter(models.Medicament.id == mid).first()
    if not medicament:
        raise HTTPException(status_code=404, detail="Médicament non trouvé")
        
    # Vérifier s'il fait bien partie de cette consultation
    if medicament not in consultation.medicaments:
        raise HTTPException(status_code=400, detail="Médicament non associé à cette consultation")
        
    # Le retirer de la collection
    consultation.medicaments.remove(medicament)
    db.commit()
    
    return {"message": "Prescription retirée avec succès"}
