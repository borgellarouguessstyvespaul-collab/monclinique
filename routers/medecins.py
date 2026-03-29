# Fichye rout (endpoints) pou jesyon doktè yo
# Dapre egzijans TP a, fòk genyen wout sa yo:
# - GET /medecins (Lister tous les médecins)
# - GET /medecins/{id}/consultations (Consultations d'un médecin)
# - POST /medecins (Créer un médecin avec Body: MedecinCreate)
# - PUT /medecins/{id} (Modifier un médecin avec path + Body)
# - DELETE /medecins/{id} (Supprimer un médecin)

from fastapi import APIRouter

router = APIRouter(prefix="/medecins", tags=["Médecins"])
