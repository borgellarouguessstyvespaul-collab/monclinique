from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Utiliser SQLite par défaut
DATABASE_URL = "sqlite:///./monclinique.db"

# Créer le moteur de base de données
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)

# Créer la session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Créer la base pour les modèles
Base = declarative_base()

# Dépendance pour obtenir la session DB
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
