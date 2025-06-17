#!/usr/bin/env python3
"""
Script de prueba para verificar que la aplicacion funciona correctamente
"""

import os
import sys
import subprocess
import time
import requests
from pathlib import Path

def test_backend():
    """Prueba el backend de la aplicacion"""
    print("🔧 Probando backend...")
    
    try:
        # Verifica que los archivos necesarios existen
        backend_dir = Path(__file__).parent / "backend"
        required_files = ["main.py", "file_comparator.py", "config.py", "requirements.txt"]
        
        for file in required_files:
            if not (backend_dir / file).exists():
                print(f"❌ Archivo faltante: {file}")
                return False
        
        print("✅ Todos los archivos del backend estan presentes")
        
        # Verifica las dependencias de Python
        try:
            import fastapi
            import pandas
            import uvicorn
            print("✅ Todas las dependencias de Python estan instaladas")
        except ImportError as e:
            print(f"❌ Dependencia faltante: {e}")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Error durante la prueba del backend: {e}")
        return False

def test_frontend():
    """Prueba el frontend de la aplicacion"""
    print("🌐 Probando frontend...")
    
    try:
        # Verifica que los archivos necesarios existen
        frontend_dir = Path(__file__).parent / "frontend"
        required_files = ["package.json", "next.config.ts"]
        
        for file in required_files:
            if not (frontend_dir / file).exists():
                print(f"❌ Archivo faltante: {file}")
                return False
        
        # Verifica que el componente principal existe
        component_file = frontend_dir / "src" / "components" / "FileComparatorDashboard.tsx"
        if not component_file.exists():
            print("❌ Componente principal faltante")
            return False
        
        print("✅ Todos los archivos del frontend estan presentes")
        
        # Verifica Node.js y npm
        try:
            result = subprocess.run(["node", "--version"], 
                                  capture_output=True, text=True, timeout=5)
            if result.returncode == 0:
                print(f"✅ Node.js detectado: {result.stdout.strip()}")
            else:
                print("❌ Node.js no encontrado")
                return False
        except:
            print("❌ Node.js no encontrado")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Error durante la prueba del frontend: {e}")
        return False

def test_scripts():
    """Prueba los scripts de inicio"""
    print("📜 Probando scripts...")
    
    try:
        scripts = ["start_dev.py", "start_production.py", "demarrer_application.bat"]
        
        for script in scripts:
            if not (Path(__file__).parent / script).exists():
                print(f"❌ Script faltante: {script}")
                return False
        
        print("✅ Todos los scripts estan presentes")
        return True
        
    except Exception as e:
        print(f"❌ Error durante la prueba de scripts: {e}")
        return False

def test_examples():
    """Prueba los archivos de ejemplo"""
    print("📁 Probando archivos de ejemplo...")
    
    try:
        examples_dir = Path(__file__).parent / "examples"
        if not examples_dir.exists():
            print("❌ Carpeta examples faltante")
            return False
        
        example_files = ["maquinas_referencia.csv", "maquinas_nuevas.csv"]
        
        for file in example_files:
            if not (examples_dir / file).exists():
                print(f"❌ Archivo de ejemplo faltante: {file}")
                return False
        
        print("✅ Todos los archivos de ejemplo estan presentes")
        return True
        
    except Exception as e:
        print(f"❌ Error durante la prueba de ejemplos: {e}")
        return False

def main():
    """Funcion principal de pruebas"""
    print("=" * 60)
    print("🧪 PRUEBA DE LA APLICACION ALTICE FILE COMPARATOR")
    print("=" * 60)
    print()
    
    tests = [
        ("Backend", test_backend),
        ("Frontend", test_frontend),
        ("Scripts", test_scripts),
        ("Ejemplos", test_examples)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        print(f"🔍 Prueba: {test_name}")
        result = test_func()
        results.append((test_name, result))
        print()
    
    # Resumen de resultados
    print("=" * 60)
    print("📊 RESUMEN DE PRUEBAS")
    print("=" * 60)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✅ EXITOSO" if result else "❌ FALLIDO"
        print(f"{test_name}: {status}")
        if result:
            passed += 1
    
    print()
    print(f"Resultado: {passed}/{total} pruebas exitosas")
    
    if passed == total:
        print("🎉 ¡Todas las pruebas fueron exitosas! La aplicacion esta lista.")
        print()
        print("🚀 Para iniciar la aplicacion:")
        print("   - Haz doble clic en 'demarrer_application.bat'")
        print("   - O ejecuta: python start_dev.py")
    else:
        print("⚠️ Algunas pruebas fallaron. Revisa los errores anteriores.")
    
    print("=" * 60)

if __name__ == "__main__":
    main() 