# Fichye rout (endpoints) pou jesyon dosye medikal
# Dapre egzijans TP a, fòk genyen wout sa yo (One-to-One avek Pasyan):
# - POST /dossiers (Créer un dossier médical avec Body: DossierCreate)
# - PUT /dossiers/{patient_id} (Mettre à jour le dossier avec path + Body)

from fastapi import APIRouter

router = APIRouter(prefix="/dossiers", tags=["Dossiers Médicaux"])
