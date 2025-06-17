@echo off
chcp 65001 >nul
title Altice File Comparator - Lanzador de Aplicacion

echo.
echo ============================================================
echo ALTICE FILE COMPARATOR - LANZADOR DE APLICACION
echo ============================================================
echo.

:: Verifica si Python esta instalado
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python no esta instalado o no esta en el PATH
    echo.
    echo Por favor instale Python desde: https://python.org
    echo.
    pause
    exit /b 1
)

:: Verifica si Node.js esta instalado
node --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Node.js no esta instalado o no esta en el PATH
    echo.
    echo Por favor instale Node.js desde: https://nodejs.org
    echo.
    pause
    exit /b 1
)

echo Python y Node.js detectados correctamente
echo.

:: Verifica si las dependencias estan instaladas
if not exist "frontend\node_modules" (
    echo Instalando dependencias del frontend...
    cd frontend
    call npm install
    if errorlevel 1 (
        echo Error al instalar dependencias del frontend
        pause
        exit /b 1
    )
    cd ..
)

if not exist "backend\venv" (
    echo Instalando dependencias del backend...
    cd backend
    call pip install -r requirements.txt
    if errorlevel 1 (
        echo Error al instalar dependencias del backend
        pause
        exit /b 1
    )
    cd ..
)

:: menu de opciones
echo Seleccione el modo de ejecucion:
echo.
echo 1. Modo Desarrollo (recomendado para desarrollo)
echo 2. Modo Produccion (optimizado para uso final)
echo 3. Solo Backend (solo API)
echo 4. Solo Frontend (solo interfaz web)
echo 5. Instalar Dependencias
echo 6. Salir
echo.

set /p choice="Ingrese su eleccion (1-6): "

if "%choice%"=="1" goto dev_mode
if "%choice%"=="2" goto prod_mode
if "%choice%"=="3" goto backend_only
if "%choice%"=="4" goto frontend_only
if "%choice%"=="5" goto install_deps
if "%choice%"=="6" goto exit
goto invalid_choice

:dev_mode
echo.
echo Iniciando modo desarrollo...
echo.
python start_dev.py
goto end

:prod_mode
echo.
echo Iniciando modo produccion...
echo.
python start_production.py
goto end

:backend_only
echo.
echo Iniciando solo el backend...
echo.
cd backend
python main.py
goto end

:frontend_only
echo.
echo Iniciando solo el frontend...
echo.
cd frontend
call npm run dev
goto end

:install_deps
echo.
echo Instalando dependencias...
echo.

:: Instala dependencias del backend
echo Instalando dependencias del backend...
cd backend
call pip install -r requirements.txt
if errorlevel 1 (
    echo Error al instalar dependencias del backend
    pause
    exit /b 1
)
cd ..

:: Instala dependencias del frontend
echo Instalando dependencias del frontend...
cd frontend
call npm install
if errorlevel 1 (
    echo Error al instalar dependencias del frontend
    pause
    exit /b 1
)
cd ..

echo Todas las dependencias instaladas correctamente
echo.
pause
goto menu

:invalid_choice
echo.
echo Opcion invalida. Por favor seleccione 1-6.
echo.
pause
goto menu

:end
echo.
echo Gracias por usar Altice File Comparator!
echo.
pause

:exit
echo.
echo Hasta luego!
echo.
timeout /t 2 >nul
exit /b 0 