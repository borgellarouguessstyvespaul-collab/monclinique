from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import engine, Base
from routers import patients, medecins, consultations, medicaments, prescriptions, dossiers
import models

# Créer les tables dans la base de données
Base.metadata.create_all(bind=engine)

# Initialiser l'application FastAPI
app = FastAPI(
    title="MonClinique API",
    description="API pour la gestion d'une clinique médicale",
    version="1.0.0"
)

# Ajouter CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inclure les routers
app.include_router(patients.router)
app.include_router(medecins.router)
app.include_router(consultations.router)
app.include_router(medicaments.router)
app.include_router(prescriptions.router)
app.include_router(dossiers.router)

# Route de test
@app.get("/")
def read_root():
    return {"message": "Bienvenue sur l'API MonClinique!"}

@app.get("/health")
def health_check():
    return {"status": "Ok", "message": "Le serveur fonctionne correctement"}
