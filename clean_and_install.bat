@echo off
chcp 65001 >nul
title Limpieza e Instalacion - Altice File Comparator

echo.
echo ============================================================
echo LIMPIEZA E INSTALACION - ALTICE FILE COMPARATOR
echo ============================================================
echo.

echo Limpiando instalaciones anteriores...
echo.

:: Limpia el frontend
echo Limpiando frontend...
cd frontend2
if exist node_modules rmdir /s /q node_modules
if exist .next rmdir /s /q .next
if exist package-lock.json del package-lock.json
cd ..

:: Limpia el backend
echo Limpiando backend...
cd backend
if exist __pycache__ rmdir /s /q __pycache__
if exist venv rmdir /s /q venv
if exist *.log del *.log
cd ..

echo.
echo Instalando dependencias...
echo.

:: Instala dependencias del frontend
echo Instalando dependencias de Node.js...
cd frontend2
call npm install
if errorlevel 1 (
    echo ERROR: No se pudieron instalar las dependencias de Node.js
    pause
    exit /b 1
)
cd ..

:: Instala dependencias del backend
echo Instalando dependencias de Python...
cd backend
call pip install -r requirements.txt
if errorlevel 1 (
    echo ERROR: No se pudieron instalar las dependencias de Python
    pause
    exit /b 1
)
cd ..

echo.
echo ============================================================
echo ¡INSTALACION COMPLETADA EXITOSAMENTE!
echo ============================================================
echo.
echo Ahora puedes iniciar la aplicacion con:
echo - demarrer_application.bat
echo - o python start_dev.py
echo.
pause 