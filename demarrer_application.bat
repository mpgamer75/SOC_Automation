@echo off
chcp 65001 >nul
echo ========================================
echo 🚀 ALTICE FILE COMPARATOR
echo ========================================
echo.
echo Elige el modo de inicio:
echo.
echo 1. Modo desarrollo (recomendado)
echo 2. Modo producción
echo 3. Solo backend
echo 4. Solo frontend
echo.
set /p eleccion="Tu elección (1-4): "

if "%eleccion%"=="1" (
    echo.
    echo 🚀 Iniciando en modo desarrollo...
    python start_dev.py
) else if "%eleccion%"=="2" (
    echo.
    echo 🚀 Iniciando en modo producción...
    python start_production.py
) else if "%eleccion%"=="3" (
    echo.
    echo 🔧 Iniciando solo el backend...
    cd backend
    python main.py
) else if "%eleccion%"=="4" (
    echo.
    echo 🌐 Iniciando solo el frontend...
    cd frontend
    npm run dev
) else (
    echo.
    echo ❌ Elección inválida
    pause
) 