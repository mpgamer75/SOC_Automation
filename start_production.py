#!/usr/bin/env python3
"""
Script de inicio para produccion
Lanza el backend y frontend en paralelo para produccion
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
        """Busca la ruta de npm en el sistema"""
        # Proba varias rutas posibles
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
                    print(f"✅ npm encontrado: {path}")
                    return path
            except:
                continue
        
        # Si npm no se encuentra, intentar con node
        try:
            result = subprocess.run(["node", "--version"], 
                                  capture_output=True, text=True, timeout=5)
            if result.returncode == 0:
                print("⚠️ npm no encontrado, usando npx...")
                return "npx"
        except:
            pass
        
        raise FileNotFoundError("npm no encontrado. Por favor instala Node.js y npm.")
        
    def start_backend(self):
        """Inicia el servidor backend"""
        print("🚀 Iniciando backend...")
        backend_dir = Path(__file__).parent / "backend"
        os.chdir(backend_dir)
        
        try:
            self.backend_process = subprocess.Popen([
                sys.executable, "main.py"
            ], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            
            print(f"✅ Backend iniciado (PID: {self.backend_process.pid})")
            print("📍 API disponible en: http://localhost:8000")
            
        except Exception as e:
            print(f"❌ Error al iniciar el backend: {e}")
            sys.exit(1)
    
    def start_frontend(self):
        """Inicia el servidor frontend"""
        print("🚀 Iniciando frontend...")
        frontend_dir = Path(__file__).parent / "frontend"
        os.chdir(frontend_dir)
        
        try:
            
            npm_path = self.find_npm()
            
            # Build para produccion primero
            print("📦 Construyendo frontend para produccion...")
            build_process = subprocess.run([
                npm_path, "run", "build"
            ], capture_output=True, text=True, timeout=120)
            
            if build_process.returncode != 0:
                print(f"❌ Error durante la construccion: {build_process.stderr}")
                sys.exit(1)
            
            print("✅ Construccion completada exitosamente")
            
            # Inicia el servidor de produccion
            self.frontend_process = subprocess.Popen([
                npm_path, "run", "start"
            ], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            
            print(f"✅ Frontend iniciado (PID: {self.frontend_process.pid})")
            print("📍 Interfaz disponible en: http://localhost:3000")
            
        except Exception as e:
            print(f"❌ Error al iniciar el frontend: {e}")
            sys.exit(1)
    
    def monitor_processes(self):
        """Monitorea los procesos y muestra los logs"""
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
        
        # Inicia los hilos de monitoreo
        backend_thread = threading.Thread(target=monitor_backend, daemon=True)
        frontend_thread = threading.Thread(target=monitor_frontend, daemon=True)
        
        backend_thread.start()
        frontend_thread.start()
    
    def stop_services(self):
        """Detiene todos los servicios"""
        print("\n🛑 Deteniendo servicios...")
        self.running = False
        
        if self.backend_process:
            self.backend_process.terminate()
            print("✅ Backend detenido")
        
        if self.frontend_process:
            self.frontend_process.terminate()
            print("✅ Frontend detenido")
    
    def signal_handler(self, signum, frame):
        """Manejador de señales para detencion limpia"""
        print(f"\n📡 Señal recibida ({signum}), deteniendo...")
        self.stop_services()
        sys.exit(0)
    
    def run(self):
        """Lanza la aplicacion completa"""
        print("=" * 60)
        print("🎯 ALTICE FILE COMPARATOR - SERVIDOR DE PRODUCCION")
        print("=" * 60)
        
        # Configuracion de los manejadores de señal
        signal.signal(signal.SIGINT, self.signal_handler)
        signal.signal(signal.SIGTERM, self.signal_handler)
        
        try:
            
            self.start_backend()
            time.sleep(3)  # Espera a que el backend este listo
            
            
            self.start_frontend()
            time.sleep(5)  # Espera a que el frontend este listo
            
            
            self.monitor_processes()
            
            print("\n" + "=" * 60)
            print("🎉 ¡APLICACION WEB INICIADA EXITOSAMENTE!")
            print("=" * 60)
            print("🌐 Frontend: http://localhost:3000")
            print("🔧 Backend API: http://localhost:8000")
            print("📚 Documentacion API: http://localhost:8000/docs")
            print("=" * 60)
            print("💡 Presiona Ctrl+C para detener la aplicacion")
            print("=" * 60)
            
            # Mantiene la aplicacion activa
            while self.running:
                time.sleep(1)
                
        except KeyboardInterrupt:
            print("\n📡 Detencion solicitada por el usuario...")
        except Exception as e:
            print(f"❌ Error inesperado: {e}")
        finally:
            self.stop_services()

if __name__ == "__main__":
    server = ProductionServer()
    server.run() 