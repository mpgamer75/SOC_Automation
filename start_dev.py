#!/usr/bin/env python3
"""
Script de démarrage pour le développement
Lance le backend et le frontend en mode développement
"""

import subprocess
import sys
import os
import time
import signal
import threading
from pathlib import Path

class DevServer:
    def __init__(self):
        self.backend_process = None
        self.frontend_process = None
        self.running = True
        
    def find_npm(self):
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
                    print(f"✅ npm trouvé: {path}")
                    return path
            except:
                continue
        
        raise FileNotFoundError("npm non trouvé. Veuillez installer Node.js et npm.")
        
    def check_dependencies(self):
        """Vérifie et installe les dépendances si nécessaire"""
        print("🔍 Vérification des dépendances...")
        
        # Vérifier les dépendances du backend
        backend_dir = Path(__file__).parent / "backend"
        if not (backend_dir / "venv").exists():
            print("📦 Installation des dépendances Python...")
            try:
                subprocess.run([
                    sys.executable, "-m", "pip", "install", "-r", "requirements.txt"
                ], cwd=backend_dir, check=True)
                print("✅ Dépendances Python installées")
            except subprocess.CalledProcessError as e:
                print(f"❌ Erreur lors de l'installation des dépendances Python: {e}")
                return False
        
        # Vérifier les dépendances du frontend
        frontend_dir = Path(__file__).parent / "frontend"
        if not (frontend_dir / "node_modules").exists():
            print("📦 Installation des dépendances Node.js...")
            try:
                npm_path = self.find_npm()
                subprocess.run([npm_path, "install"], cwd=frontend_dir, check=True)
                print("✅ Dépendances Node.js installées")
            except subprocess.CalledProcessError as e:
                print(f"❌ Erreur lors de l'installation des dépendances Node.js: {e}")
                return False
        
        return True
        
    def start_backend(self):
        """Démarre le serveur backend en mode développement"""
        print("🚀 Démarrage du backend (mode développement)...")
        backend_dir = Path(__file__).parent / "backend"
        os.chdir(backend_dir)
        
        try:
            self.backend_process = subprocess.Popen([
                sys.executable, "main.py"
            ], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            
            print(f"✅ Backend démarré (PID: {self.backend_process.pid})")
            print("📍 API disponible sur: http://localhost:8000")
            
        except Exception as e:
            print(f"❌ Erreur lors du démarrage du backend: {e}")
            sys.exit(1)
    
    def start_frontend(self):
        """Démarre le serveur frontend en mode développement"""
        print("🚀 Démarrage du frontend (mode développement)...")
        frontend_dir = Path(__file__).parent / "frontend"
        os.chdir(frontend_dir)
        
        try:
            npm_path = self.find_npm()
            
            # Démarrer le serveur de développement
            self.frontend_process = subprocess.Popen([
                npm_path, "run", "dev"
            ], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            
            print(f"✅ Frontend démarré (PID: {self.frontend_process.pid})")
            print("📍 Interface disponible sur: http://localhost:3000")
            
        except Exception as e:
            print(f"❌ Erreur lors du démarrage du frontend: {e}")
            sys.exit(1)
    
    def monitor_processes(self):
        """Surveille les processus et affiche les logs"""
        def monitor_backend():
            if self.backend_process:
                for line in iter(self.backend_process.stdout.readline, ''):
                    if line:
                        print(f"[BACKEND] {line.strip()}")
        
        def monitor_frontend():
            if self.frontend_process:
                for line in iter(self.frontend_process.stdout.readline, ''):
                    if line:
                        print(f"[FRONTEND] {line.strip()}")
        
        backend_thread = threading.Thread(target=monitor_backend, daemon=True)
        frontend_thread = threading.Thread(target=monitor_frontend, daemon=True)
        
        backend_thread.start()
        frontend_thread.start()
    
    def stop_services(self):
        """Arrête tous les services"""
        print("\n🛑 Arrêt des services...")
        self.running = False
        
        if self.backend_process:
            self.backend_process.terminate()
            print("✅ Backend arrêté")
        
        if self.frontend_process:
            self.frontend_process.terminate()
            print("✅ Frontend arrêté")
    
    def signal_handler(self, signum, frame):
        """Gestionnaire de signal pour l'arrêt propre"""
        print(f"\n📡 Signal reçu ({signum}), arrêt en cours...")
        self.stop_services()
        sys.exit(0)
    
    def run(self):
        """Lance l'application en mode développement"""
        print("=" * 60)
        print("🔧 ALTICE FILE COMPARATOR - MODE DÉVELOPPEMENT")
        print("=" * 60)
        
        signal.signal(signal.SIGINT, self.signal_handler)
        signal.signal(signal.SIGTERM, self.signal_handler)
        
        try:
            # Vérifier les dépendances
            if not self.check_dependencies():
                print("❌ Impossible de vérifier les dépendances")
                sys.exit(1)
            
            # Démarrer le backend
            self.start_backend()
            time.sleep(3)
            
            # Démarrer le frontend
            self.start_frontend()
            time.sleep(5)
            
            # Démarrer la surveillance
            self.monitor_processes()
            
            print("\n" + "=" * 60)
            print("🎉 APPLICATION WEB DÉMARRÉE EN MODE DÉVELOPPEMENT!")
            print("=" * 60)
            print("🌐 Frontend: http://localhost:3000")
            print("🔧 Backend API: http://localhost:8000")
            print("📚 Documentation API: http://localhost:8000/docs")
            print("=" * 60)
            print("💡 Appuyez sur Ctrl+C pour arrêter l'application")
            print("=" * 60)
            
            while self.running:
                time.sleep(1)
                
        except KeyboardInterrupt:
            print("\n📡 Arrêt demandé par l'utilisateur...")
        except Exception as e:
            print(f"❌ Erreur inattendue: {e}")
        finally:
            self.stop_services()

if __name__ == "__main__":
    server = DevServer()
    server.run() 