#!/usr/bin/env python3
"""
Script de test pour l'API IDFAD
Développé par Greenfad
"""

import requests
import json
import time
import sys
from datetime import datetime

# Configuration des tests
BASE_URL = "http://localhost:5001"
API_BASE = f"{BASE_URL}/api"
IDENTITY_API = f"{API_BASE}/identity"

def print_test_header(test_name):
    """Affiche l'en-tête d'un test"""
    print(f"\n{'='*60}")
    print(f"TEST: {test_name}")
    print(f"{'='*60}")

def print_test_result(success, message):
    """Affiche le résultat d'un test"""
    status = "✅ SUCCÈS" if success else "❌ ÉCHEC"
    print(f"{status}: {message}")

def test_api_health():
    """Test de l'endpoint de santé de l'API"""
    print_test_header("Test de Santé de l'API")
    
    try:
        response = requests.get(f"{API_BASE}/health", timeout=5)
        
        if response.status_code == 200:
            data = response.json()
            print_test_result(True, f"API accessible - Status: {data.get('status')}")
            print(f"Service: {data.get('service')}")
            print(f"Version: {data.get('version')}")
            print(f"Société: {data.get('company')}")
            return True
        else:
            print_test_result(False, f"Code de statut inattendu: {response.status_code}")
            return False
            
    except requests.exceptions.ConnectionError:
        print_test_result(False, "Impossible de se connecter à l'API")
        return False
    except Exception as e:
        print_test_result(False, f"Erreur: {str(e)}")
        return False

def test_identity_health():
    """Test de l'endpoint de santé du service d'identité"""
    print_test_header("Test de Santé du Service d'Identité")
    
    try:
        response = requests.get(f"{IDENTITY_API}/health", timeout=5)
        
        if response.status_code == 200:
            data = response.json()
            print_test_result(True, f"Service d'identité accessible - Status: {data.get('status')}")
            print(f"Service: {data.get('service')}")
            print(f"Société: {data.get('company')}")
            return True
        else:
            print_test_result(False, f"Code de statut inattendu: {response.status_code}")
            return False
            
    except requests.exceptions.ConnectionError:
        print_test_result(False, "Impossible de se connecter au service d'identité")
        return False
    except Exception as e:
        print_test_result(False, f"Erreur: {str(e)}")
        return False

def test_citizen_registration():
    """Test d'enregistrement d'un citoyen"""
    print_test_header("Test d'Enregistrement de Citoyen")
    
    # Données de test
    test_citizen = {
        "first_name": "Jean",
        "last_name": "Dupont",
        "middle_name": "Pierre",
        "date_of_birth": "1990-05-15",
        "place_of_birth": "Yaoundé",
        "gender": "M",
        "phone_number": "+237123456789",
        "email": "jean.dupont@email.com",
        "address_line1": "123 Rue de la Paix",
        "address_line2": "Quartier Central",
        "city": "Yaoundé",
        "region": "Centre",
        "postal_code": "1000",
        "country": "Cameroun",
        "father_name": "Paul Dupont",
        "mother_name": "Marie Dupont",
        "marital_status": "single",
        "pin": "1234"
    }
    
    try:
        response = requests.post(
            f"{IDENTITY_API}/citizens",
            json=test_citizen,
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        
        if response.status_code == 201:
            data = response.json()
            print_test_result(True, "Citoyen enregistré avec succès")
            print(f"ID National généré: {data.get('national_id')}")
            print(f"Message: {data.get('message')}")
            return data.get('citizen', {}).get('id')
        else:
            error_data = response.json() if response.headers.get('content-type') == 'application/json' else {}
            print_test_result(False, f"Erreur d'enregistrement: {error_data.get('error', 'Erreur inconnue')}")
            return None
            
    except requests.exceptions.ConnectionError:
        print_test_result(False, "Impossible de se connecter au service d'identité")
        return None
    except Exception as e:
        print_test_result(False, f"Erreur: {str(e)}")
        return None

def test_citizen_search():
    """Test de recherche de citoyens"""
    print_test_header("Test de Recherche de Citoyens")
    
    # Critères de recherche
    search_criteria = {
        "first_name": "Jean",
        "last_name": "Dupont"
    }
    
    try:
        response = requests.post(
            f"{IDENTITY_API}/citizens/search",
            json=search_criteria,
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            citizens = data.get('citizens', [])
            print_test_result(True, f"Recherche effectuée - {len(citizens)} résultat(s) trouvé(s)")
            
            for citizen in citizens[:3]:  # Afficher les 3 premiers résultats
                print(f"  - {citizen.get('first_name')} {citizen.get('last_name')} (ID: {citizen.get('national_id')})")
            
            return len(citizens) > 0
        else:
            error_data = response.json() if response.headers.get('content-type') == 'application/json' else {}
            print_test_result(False, f"Erreur de recherche: {error_data.get('error', 'Erreur inconnue')}")
            return False
            
    except requests.exceptions.ConnectionError:
        print_test_result(False, "Impossible de se connecter au service d'identité")
        return False
    except Exception as e:
        print_test_result(False, f"Erreur: {str(e)}")
        return False

def test_statistics():
    """Test de récupération des statistiques"""
    print_test_header("Test des Statistiques")
    
    try:
        response = requests.get(f"{IDENTITY_API}/statistics", timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            print_test_result(True, "Statistiques récupérées avec succès")
            
            citizens = data.get('citizens', {})
            print(f"  - Total citoyens: {citizens.get('total', 0)}")
            print(f"  - Citoyens actifs: {citizens.get('active', 0)}")
            print(f"  - Citoyens suspendus: {citizens.get('suspended', 0)}")
            
            biometrics = data.get('biometrics', {})
            print(f"  - Total données biométriques: {biometrics.get('total', 0)}")
            print(f"  - Empreintes: {biometrics.get('fingerprint', 0)}")
            print(f"  - Reconnaissance faciale: {biometrics.get('face', 0)}")
            
            return True
        else:
            error_data = response.json() if response.headers.get('content-type') == 'application/json' else {}
            print_test_result(False, f"Erreur de récupération: {error_data.get('error', 'Erreur inconnue')}")
            return False
            
    except requests.exceptions.ConnectionError:
        print_test_result(False, "Impossible de se connecter au service d'identité")
        return False
    except Exception as e:
        print_test_result(False, f"Erreur: {str(e)}")
        return False

def test_authentication():
    """Test d'authentification"""
    print_test_header("Test d'Authentification")
    
    # Données d'authentification de test
    auth_data = {
        "national_id": "202505151234",  # ID généré lors de l'enregistrement
        "auth_method": "pin",
        "pin": "1234",
        "service_requested": "consultation"
    }
    
    try:
        response = requests.post(
            f"{IDENTITY_API}/authenticate",
            json=auth_data,
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            print_test_result(True, "Authentification réussie")
            print(f"  - Citoyen: {data.get('full_name')}")
            print(f"  - Score de risque: {data.get('risk_score')}")
            print(f"  - Token de session: {data.get('session_token', '')[:20]}...")
            return True
        elif response.status_code == 401:
            print_test_result(False, "Authentification échouée (identifiants incorrects)")
            return False
        elif response.status_code == 404:
            print_test_result(False, "Citoyen non trouvé")
            return False
        else:
            error_data = response.json() if response.headers.get('content-type') == 'application/json' else {}
            print_test_result(False, f"Erreur d'authentification: {error_data.get('error', 'Erreur inconnue')}")
            return False
            
    except requests.exceptions.ConnectionError:
        print_test_result(False, "Impossible de se connecter au service d'identité")
        return False
    except Exception as e:
        print_test_result(False, f"Erreur: {str(e)}")
        return False

def run_all_tests():
    """Exécute tous les tests"""
    print("🚀 DÉBUT DES TESTS DE L'API IDFAD - GREENFAD")
    print(f"Timestamp: {datetime.now().isoformat()}")
    
    tests = [
        ("Santé API Générale", test_api_health),
        ("Santé Service Identité", test_identity_health),
        ("Enregistrement Citoyen", test_citizen_registration),
        ("Recherche Citoyens", test_citizen_search),
        ("Statistiques", test_statistics),
        ("Authentification", test_authentication)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print_test_result(False, f"Erreur lors du test {test_name}: {str(e)}")
            results.append((test_name, False))
        
        time.sleep(1)  # Pause entre les tests
    
    # Résumé des résultats
    print_test_header("RÉSUMÉ DES TESTS")
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅" if result else "❌"
        print(f"{status} {test_name}")
    
    print(f"\nRésultat global: {passed}/{total} tests réussis")
    
    if passed == total:
        print("🎉 TOUS LES TESTS SONT PASSÉS AVEC SUCCÈS!")
        return True
    else:
        print("⚠️  CERTAINS TESTS ONT ÉCHOUÉ")
        return False

if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)

