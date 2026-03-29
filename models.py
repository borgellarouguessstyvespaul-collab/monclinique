# Fichye pou modèl baz done yo (SQLAlchemy Models)
# Moun ki responsab la ap gen pou:
# - Itilize SQLAlchemy ORM epi defini classes ki erite de "Base".
# - Defini cles etrangeres ak "ForeignKey", e relasyon ak "relationship()".
#
# Tab pou kreye dapre TP a:
# 1. Patient
# 2. DossierMedical (One-to-One ak Patient)
# 3. Medecin
# 4. Consultation (One-to-Many ak Medecin; One-to-Many ak Patient)
# 5. Medicament
# 6. Table pivot pour Prescription (Many-to-Many antre Consultation ak Medicament)

