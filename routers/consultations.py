# Fichye rout (endpoints) pou jesyon konsiltasyon
# Dapre egzijans TP a, fòk genyen wout sa yo:
# - GET /consultations (Lister toutes les consultations)
# - GET /consultations/{id} (Consultation + médicaments prescrits)
# - POST /consultations (Créer une consultation avec Body: ConsultCreate)
# - DELETE /consultations/{id} (Supprimer une consultation)

from fastapi import APIRouter

router = APIRouter(prefix="/consultations", tags=["Consultations"])
