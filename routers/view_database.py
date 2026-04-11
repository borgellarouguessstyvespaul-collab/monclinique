import urllib.request
import json

API_URL = "http://localhost:8000"

def get_data(endpoint):
    """Récupérer les données d'un endpoint"""
    try:
        req = urllib.request.Request(
            f"{API_URL}/{endpoint}/",
            headers={"Content-Type": "application/json"},
            method="GET"
        )
        
        with urllib.request.urlopen(req) as response:
            return json.loads(response.read().decode('utf-8'))
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return []

print("="*70)
print("📊 CONTENU DE LA BASE DE DONNÉES - MONCLINIQUE")
print("="*70)

# ===== MÉDECINS =====
print("\n👨‍⚕️ MÉDECINS")
print("-" * 70)
medecins = get_data("medecins")
if medecins:
    print(f"{'ID':<4} {'Nom':<20} {'Spécialité':<20} {'Email':<25}")
    print("-" * 70)
    for med in medecins:
        print(f"{med['id']:<4} {med['prenom']} {med['nom']:<15} {med['specialite']:<20} {med['email']:<25}")
    print(f"\n✓ Total: {len(medecins)} médecins")

# ===== PATIENTS =====
print("\n👥 PATIENTS")
print("-" * 70)
patients = get_data("patients")
if patients:
    print(f"{'ID':<4} {'Nom':<20} {'Email':<30} {'Téléphone':<15}")
    print("-" * 70)
    for pat in patients:
        email = pat.get('email', 'N/A')[:28]
        tel = pat.get('telephone', 'N/A')
        print(f"{pat['id']:<4} {pat['prenom']} {pat['nom']:<15} {email:<30} {tel:<15}")
    print(f"\n✓ Total: {len(patients)} patients")

# ===== MÉDICAMENTS =====
print("\n💊 MÉDICAMENTS")
print("-" * 70)
medicaments = get_data("medicaments")
if medicaments:
    print(f"{'ID':<4} {'Nom':<20} {'Dosage':<12} {'Forme':<15} {'Prix':<8}")
    print("-" * 70)
    for med in medicaments:
        dosage = med.get('dosage', 'N/A')
        forme = med.get('forme', 'N/A')
        prix = f"{med.get('prix', 0):.2f}€"
        print(f"{med['id']:<4} {med['nom']:<20} {dosage:<12} {forme:<15} {prix:<8}")
    print(f"\n✓ Total: {len(medicaments)} médicaments")

# ===== CONSULTATIONS =====
print("\n📝 CONSULTATIONS")
print("-" * 70)
consultations = get_data("consultations")
if consultations:
    print(f"{'ID':<4} {'Patient':<15} {'Médecin':<15} {'Diagnostic':<25}")
    print("-" * 70)
    for cons in consultations:
        patient_name = ""
        doctor_name = ""
        
        # Chercher le nom du patient
        for pat in patients:
            if pat['id'] == cons['patient_id']:
                patient_name = f"{pat['prenom']} {pat['nom']}"
                break
        
        # Chercher le nom du médecin
        for med in medecins:
            if med['id'] == cons['medecin_id']:
                doctor_name = f"Dr {med['prenom']}"
                break
        
        diagnostic = cons.get('diagnostic', 'N/A')[:23]
        print(f"{cons['id']:<4} {patient_name:<15} {doctor_name:<15} {diagnostic:<25}")
        if cons.get('medicaments'):
            meds_str = ", ".join([m['nom'] for m in cons['medicaments']])
            print(f"     → Médicaments: {meds_str}")
    
    print(f"\n✓ Total: {len(consultations)} consultations")

print("\n" + "="*70)
print(f"✅ BASE DE DONNÉES REMPLIE AVEC SUCCÈS")
print("="*70)
print("\n🔗 Pour voir plus de détails:")
print("   📍 Swagger UI: http://localhost:8000/docs")
print("   📍 ReDoc: http://localhost:8000/redoc")
print("\n💾 Fichier de base de données: monclinique.db")
print("="*70)
