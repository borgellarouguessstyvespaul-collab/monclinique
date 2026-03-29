# Fichye rout (endpoints) pou jesyon medikaman
# Dapre egzijans TP a, fòk genyen wout sa yo:
# - GET /medicaments (Lister tous les médicaments)
# - POST /medicaments (Ajouter un médicament avec Body: MedCreate)

from fastapi import APIRouter

router = APIRouter(prefix="/medicaments", tags=["Médicaments"])
