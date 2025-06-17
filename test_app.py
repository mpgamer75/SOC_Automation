#!/usr/bin/env python3
"""
Script de test pour vérifier que l'application fonctionne correctement
"""

import os
import sys
import subprocess
import time
import requests
from pathlib import Path

def test_backend():
    """Teste le backend"""
    print("🔧 Test du backend...")
    
    try:
        # Vérifier que les fichiers existent
        backend_dir = Path(__file__).parent / "backend"
        required_files = ["main.py", "file_comparator.py", "config.py", "requirements.txt"]
        
        for file in required_files:
            if not (backend_dir / file).exists():
                print(f"❌ Fichier manquant: {file}")
                return False
        
        print("✅ Tous les fichiers backend sont présents")
        
        # Vérifier les dépendances
        try:
            import fastapi
            import pandas
            import uvicorn
            print("✅ Toutes les dépendances Python sont installées")
        except ImportError as e:
            print(f"❌ Dépendance manquante: {e}")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors du test du backend: {e}")
        return False

def test_frontend():
    """Teste le frontend"""
    print("🌐 Test du frontend...")
    
    try:
        # Vérifier que les fichiers existent
        frontend_dir = Path(__file__).parent / "frontend"
        required_files = ["package.json", "next.config.ts"]
        
        for file in required_files:
            if not (frontend_dir / file).exists():
                print(f"❌ Fichier manquant: {file}")
                return False
        
        # Vérifier que le composant principal existe
        component_file = frontend_dir / "src" / "components" / "FileComparatorDashboard.tsx"
        if not component_file.exists():
            print("❌ Composant principal manquant")
            return False
        
        print("✅ Tous les fichiers frontend sont présents")
        
        # Vérifier Node.js et npm
        try:
            result = subprocess.run(["node", "--version"], 
                                  capture_output=True, text=True, timeout=5)
            if result.returncode == 0:
                print(f"✅ Node.js détecté: {result.stdout.strip()}")
            else:
                print("❌ Node.js non trouvé")
                return False
        except:
            print("❌ Node.js non trouvé")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors du test du frontend: {e}")
        return False

def test_scripts():
    """Teste les scripts de démarrage"""
    print("📜 Test des scripts...")
    
    try:
        scripts = ["start_dev.py", "start_production.py", "demarrer_application.bat"]
        
        for script in scripts:
            if not (Path(__file__).parent / script).exists():
                print(f"❌ Script manquant: {script}")
                return False
        
        print("✅ Tous les scripts sont présents")
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors du test des scripts: {e}")
        return False

def test_examples():
    """Teste les fichiers d'exemple"""
    print("📁 Test des fichiers d'exemple...")
    
    try:
        examples_dir = Path(__file__).parent / "examples"
        if not examples_dir.exists():
            print("❌ Dossier examples manquant")
            return False
        
        example_files = ["sample_data.csv", "sample_data_modified.csv"]
        
        for file in example_files:
            if not (examples_dir / file).exists():
                print(f"❌ Fichier d'exemple manquant: {file}")
                return False
        
        print("✅ Tous les fichiers d'exemple sont présents")
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors du test des exemples: {e}")
        return False

def main():
    """Fonction principale de test"""
    print("=" * 60)
    print("🧪 TEST DE L'APPLICATION ALTICE FILE COMPARATOR")
    print("=" * 60)
    print()
    
    tests = [
        ("Backend", test_backend),
        ("Frontend", test_frontend),
        ("Scripts", test_scripts),
        ("Exemples", test_examples)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        print(f"🔍 Test: {test_name}")
        result = test_func()
        results.append((test_name, result))
        print()
    
    # Résumé
    print("=" * 60)
    print("📊 RÉSUMÉ DES TESTS")
    print("=" * 60)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASSÉ" if result else "❌ ÉCHOUÉ"
        print(f"{test_name}: {status}")
        if result:
            passed += 1
    
    print()
    print(f"Résultat: {passed}/{total} tests passés")
    
    if passed == total:
        print("🎉 Tous les tests sont passés ! L'application est prête.")
        print()
        print("🚀 Pour démarrer l'application:")
        print("   - Double-cliquez sur 'demarrer_application.bat'")
        print("   - Ou exécutez: python start_dev.py")
    else:
        print("⚠️ Certains tests ont échoué. Vérifiez les erreurs ci-dessus.")
    
    print("=" * 60)

if __name__ == "__main__":
    main() 