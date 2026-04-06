#!/usr/bin/env python3
"""
Script pour afficher le contenu de toutes les tables
"""

from database import SessionLocal
import models

def show_tables():
    """Afficher le contenu de toutes les tables"""
    db = SessionLocal()
    
    try:
        print("\n" + "="*80)
        print("📊 CONTENU DES TABLES - MONCLINIQUE")
        print("="*80)
        
        # Afficher les patients
        print("\n👥 PATIENTS:")
        print("-" * 80)
        patients = db.query(models.Patient).all()
        if patients:
            print(f"{'ID':<5} {'Prénom':<15} {'Nom':<15} {'Email':<30} {'Téléphone':<15}")
            print("-" * 80)
            for p in patients:
                print(f"{p.id:<5} {p.prenom:<15} {p.nom:<15} {p.email:<30} {p.telephone:<15}")
        else:
            print("❌ Aucun patient trouvé")
        
        # Afficher les médecins
        print("\n\n👨‍⚕️ MÉDECINS:")
        print("-" * 80)
        medecins = db.query(models.Medecin).all()
        if medecins:
            print(f"{'ID':<5} {'Prénom':<15} {'Nom':<15} {'Spécialité':<20} {'Email':<25}")
            print("-" * 80)
            for m in medecins:
                print(f"{m.id:<5} {m.prenom:<15} {m.nom:<15} {m.specialite:<20} {m.email:<25}")
        else:
            print("❌ Aucun médecin trouvé")
        
        # Afficher les consultations
        print("\n\n📋 CONSULTATIONS:")
        print("-" * 80)
        consultations = db.query(models.Consultation).all()
        if consultations:
            print(f"{'ID':<5} {'Patient':<15} {'Médecin':<15} {'Diagnostic':<30} {'Date':<20}")
            print("-" * 80)
            for c in consultations:
                print(f"{c.id:<5} {c.patient_id:<15} {c.medecin_id:<15} {c.diagnostic:<30} {str(c.date_consultation):<20}")
        else:
            print("❌ Aucune consultation trouvée")
        
        # Afficher les dossiers
        print("\n\n📁 DOSSIERS MÉDICAUX:")
        print("-" * 80)
        dossiers = db.query(models.Dossier).all()
        if dossiers:
            print(f"{'ID':<5} {'Patient':<15} {'Groupe Sanguin':<20} {'Allergies':<30}")
            print("-" * 80)
            for d in dossiers:
                allergies = d.allergies if d.allergies else "Aucune"
                print(f"{d.id:<5} {d.patient_id:<15} {d.groupe_sanguin:<20} {allergies:<30}")
        else:
            print("❌ Aucun dossier trouvé")
        
        # Afficher les médicaments
        print("\n\n💊 MÉDICAMENTS:")
        print("-" * 80)
        medicaments = db.query(models.Medicament).all()
        if medicaments:
            print(f"{'ID':<5} {'Nom':<20} {'Dosage':<15} {'Forme':<15} {'Description':<25}")
            print("-" * 80)
            for m in medicaments:
                desc = m.description[:25] if m.description else ""
                print(f"{m.id:<5} {m.nom:<20} {m.dosage:<15} {m.forme:<15} {desc:<25}")
        else:
            print("❌ Aucun médicament trouvé")
        
        # Afficher les prescriptions
        print("\n\n📝 PRESCRIPTIONS:")
        print("-" * 80)
        prescriptions = db.query(models.Prescription).all()
        if prescriptions:
            print(f"{'ID':<5} {'Consultation':<15} {'Médecin':<15} {'Médicament':<15} {'Dosage':<15}")
            print("-" * 80)
            for p in prescriptions:
                print(f"{p.id:<5} {p.consultation_id:<15} {p.medecin_id:<15} {p.medicament_id:<15} {p.dosage:<15}")
        else:
            print("❌ Aucune prescription trouvée")
        
        print("\n" + "="*80)
        print(f"✅ Total: {len(patients)} patients, {len(medecins)} médecins, {len(consultations)} consultations")
        print("="*80 + "\n")
        
    except Exception as e:
        print(f"❌ Erreur: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    show_tables()
