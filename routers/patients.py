# Fichye rout (endpoints) pou jesyon pasyan yo
# Dapre egzijans TP a, fòk genyen wout sa yo:
# - GET /patients (Lister tous les patients)
# - GET /patients/{id} (Patient + dossier (One-to-One))
# - GET /patients/{id}/consultations (Consultations d'un patient)
# - POST /patients (Créer un patient avec Body: PatientCreate)
# - PUT /patients/{id} (Modifier un patient avec path + Body)
# - DELETE /patients/{id} (Supprimer un patient)

from fastapi import APIRouter

router = APIRouter(prefix="/patients", tags=["Patients"])
