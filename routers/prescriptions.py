# Fichye rout (endpoints) pou jesyon preskripsyon (table pivot Many-to-Many)
# Dapre egzijans TP a, fòk genyen wout sa yo pami Consultation ak Medicament:
# - POST /prescriptions (Prescrire un médicament avec Body: PrescriptionCreate)
# - DELETE /prescriptions/{cid}/{mid} (Retirer un médicament prescrit)

from fastapi import APIRouter

router = APIRouter(prefix="/prescriptions", tags=["Prescriptions"])
