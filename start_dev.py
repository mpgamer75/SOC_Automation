#!/usr/bin/env python3
"""
Script de démarrage simple pour le développement
"""

import subprocess
import sys
import os
import time
from pathlib import Path

def find_npm():
    """Trouve le chemin de npm"""
    possible_paths = [
        "npm",
        "C:\\Program Files\\nodejs\\npm.cmd",
        "C:\\Program Files (x86)\\nodejs\\npm.cmd",
        os.path.expanduser("~\\AppData\\Roaming\\npm\\npm.cmd"),
        os.path.expanduser("~\\AppData\\Local\\Programs\\nodejs\\npm.cmd")
    ]
    
    for path in possible_paths:
        try:
            result = subprocess.run([path, "--version"], 
                                  capture_output=True, text=True, timeout=5)
            if result.returncode == 0:
                return path
        except:
            continue
    
    return None

def main():
    print("🚀 Démarrage de l'application en mode développement...")
    
    # Vérifier npm
    npm_path = find_npm()
    if not npm_path:
        print("❌ npm non trouvé. Veuillez installer Node.js et npm.")
        print("📥 Téléchargement: https://nodejs.org/")
        return
    
    print(f"✅ npm trouvé: {npm_path}")
    
    # Démarrer le backend
    print("\n🔧 Démarrage du backend...")
    backend_dir = Path(__file__).parent / "backend"
    os.chdir(backend_dir)
    
    backend_process = subprocess.Popen([
        sys.executable, "main.py"
    ])
    
    print("✅ Backend démarré sur http://localhost:8000")
    
    # Démarrer le frontend
    print("\n🌐 Démarrage du frontend...")
    frontend_dir = Path(__file__).parent / "frontend"
    os.chdir(frontend_dir)
    
    frontend_process = subprocess.Popen([
        npm_path, "run", "dev"
    ])
    
    print("✅ Frontend démarré sur http://localhost:3000")
    
    print("\n" + "=" * 50)
    print("🎉 APPLICATION DÉMARRÉE!")
    print("=" * 50)
    print("🌐 Interface: http://localhost:3000")
    print("🔧 API: http://localhost:8000")
    print("📚 Docs: http://localhost:8000/docs")
    print("=" * 50)
    print("💡 Appuyez sur Ctrl+C pour arrêter")
    print("=" * 50)
    
    try:
        # Attendre que l'utilisateur arrête
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n🛑 Arrêt des services...")
        backend_process.terminate()
        frontend_process.terminate()
        print("✅ Services arrêtés")

if __name__ == "__main__":
    main() 