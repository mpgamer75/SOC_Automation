@echo off
chcp 65001 >nul
title 🎯 Altice File Comparator - Lanzador de Aplicación

echo.
echo ============================================================
echo 🎯 ALTICE FILE COMPARATOR - LANZADOR DE APLICACIÓN
echo ============================================================
echo.

:: Verificar si Python está instalado
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ ERROR: Python no está instalado o no está en el PATH
    echo.
    echo 💡 Por favor instale Python desde: https://python.org
    echo.
    pause
    exit /b 1
)

:: Verificar si Node.js está instalado
node --version >nul 2>&1
if errorlevel 1 (
    echo ❌ ERROR: Node.js no está instalado o no está en el PATH
    echo.
    echo 💡 Por favor instale Node.js desde: https://nodejs.org
    echo.
    pause
    exit /b 1
)

echo ✅ Python y Node.js detectados correctamente
echo.

:: Mostrar menú de opciones
echo 📋 Seleccione el modo de ejecución:
echo.
echo 1️⃣  🔧 Modo Desarrollo (recomendado para desarrollo)
echo 2️⃣  🚀 Modo Producción (optimizado para uso final)
echo 3️⃣  🔧 Solo Backend (solo API)
echo 4️⃣  🌐 Solo Frontend (solo interfaz web)
echo 5️⃣  📦 Instalar Dependencias
echo 6️⃣  🚪 Salir
echo.

set /p choice="🎯 Ingrese su elección (1-6): "

if "%choice%"=="1" goto dev_mode
if "%choice%"=="2" goto prod_mode
if "%choice%"=="3" goto backend_only
if "%choice%"=="4" goto frontend_only
if "%choice%"=="5" goto install_deps
if "%choice%"=="6" goto exit
goto invalid_choice

:dev_mode
echo.
echo 🔧 Iniciando modo desarrollo...
echo.
python start_dev.py
goto end

:prod_mode
echo.
echo 🚀 Iniciando modo producción...
echo.
python start_production.py
goto end

:backend_only
echo.
echo 🔧 Iniciando solo el backend...
echo.
cd backend
python main.py
goto end

:frontend_only
echo.
echo 🌐 Iniciando solo el frontend...
echo.
cd frontend
npm run dev
goto end

:install_deps
echo.
echo 📦 Instalando dependencias...
echo.

:: Instalar dependencias del backend
echo 🔧 Instalando dependencias del backend...
cd backend
pip install -r requirements.txt
if errorlevel 1 (
    echo ❌ Error al instalar dependencias del backend
    pause
    exit /b 1
)

:: Instalar dependencias del frontend
echo 🌐 Instalando dependencias del frontend...
cd ..\frontend
npm install
if errorlevel 1 (
    echo ❌ Error al instalar dependencias del frontend
    pause
    exit /b 1
)

echo ✅ Todas las dependencias instaladas correctamente
echo.
pause
goto menu

:invalid_choice
echo.
echo ❌ Opción inválida. Por favor seleccione 1-6.
echo.
pause
goto menu

:end
echo.
echo 🎉 ¡Gracias por usar Altice File Comparator!
echo.
pause

:exit
echo.
echo 👋 ¡Hasta luego!
echo.
timeout /t 2 >nul
exit /b 0 