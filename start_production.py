#!/usr/bin/env python3
"""
Script de démarrage pour la production
Lance le backend et le frontend en parallèle
"""

import subprocess
import sys
import os
import time
import signal
import threading
from pathlib import Path

class ProductionServer:
    def __init__(self):
        self.backend_process = None
        self.frontend_process = None
        self.running = True
        
    def find_npm(self):
        """Trouve le chemin de npm"""
        # Essayer plusieurs chemins possibles
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
        
        # Si npm n'est pas trouvé, essayer avec node
        try:
            result = subprocess.run(["node", "--version"], 
                                  capture_output=True, text=True, timeout=5)
            if result.returncode == 0:
                print("⚠️ npm non trouvé, utilisation de npx...")
                return "npx"
        except:
            pass
        
        raise FileNotFoundError("npm non trouvé. Veuillez installer Node.js et npm.")
        
    def start_backend(self):
        """Démarre le serveur backend"""
        print("🚀 Démarrage du backend...")
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
        """Démarre le serveur frontend"""
        print("🚀 Démarrage du frontend...")
        frontend_dir = Path(__file__).parent / "frontend"
        os.chdir(frontend_dir)
        
        try:
            # Trouver npm
            npm_path = self.find_npm()
            
            # Build pour la production d'abord
            print("📦 Build du frontend pour la production...")
            build_process = subprocess.run([
                npm_path, "run", "build"
            ], capture_output=True, text=True, timeout=120)
            
            if build_process.returncode != 0:
                print(f"❌ Erreur lors du build: {build_process.stderr}")
                sys.exit(1)
            
            print("✅ Build terminé avec succès")
            
            # Démarrer le serveur de production
            self.frontend_process = subprocess.Popen([
                npm_path, "run", "start"
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
        
        # Démarrer les threads de surveillance
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
        """Lance l'application complète"""
        print("=" * 60)
        print("🎯 ALTICE FILE COMPARATOR - SERVEUR DE PRODUCTION")
        print("=" * 60)
        
        # Configuration des gestionnaires de signal
        signal.signal(signal.SIGINT, self.signal_handler)
        signal.signal(signal.SIGTERM, self.signal_handler)
        
        try:
            # Démarrer le backend
            self.start_backend()
            time.sleep(3)  # Attendre que le backend soit prêt
            
            # Démarrer le frontend
            self.start_frontend()
            time.sleep(5)  # Attendre que le frontend soit prêt
            
            # Démarrer la surveillance
            self.monitor_processes()
            
            print("\n" + "=" * 60)
            print("🎉 APPLICATION WEB DÉMARRÉE AVEC SUCCÈS!")
            print("=" * 60)
            print("🌐 Frontend: http://localhost:3000")
            print("🔧 Backend API: http://localhost:8000")
            print("📚 Documentation API: http://localhost:8000/docs")
            print("=" * 60)
            print("💡 Appuyez sur Ctrl+C pour arrêter l'application")
            print("=" * 60)
            
            # Maintenir l'application en vie
            while self.running:
                time.sleep(1)
                
        except KeyboardInterrupt:
            print("\n📡 Arrêt demandé par l'utilisateur...")
        except Exception as e:
            print(f"❌ Erreur inattendue: {e}")
        finally:
            self.stop_services()

if __name__ == "__main__":
    server = ProductionServer()
    server.run() 