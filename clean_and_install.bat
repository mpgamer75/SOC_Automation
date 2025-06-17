@echo off
chcp 65001 >nul
title Nettoyage et Installation - Altice File Comparator

echo.
echo ============================================================
echo NETTOYAGE ET INSTALLATION - ALTICE FILE COMPARATOR
echo ============================================================
echo.

echo Nettoyage des anciennes installations...
echo.

:: Nettoyer le frontend
echo Nettoyage du frontend...
cd frontend
if exist node_modules rmdir /s /q node_modules
if exist .next rmdir /s /q .next
if exist package-lock.json del package-lock.json
cd ..

:: Nettoyer le backend
echo Nettoyage du backend...
cd backend
if exist __pycache__ rmdir /s /q __pycache__
if exist venv rmdir /s /q venv
if exist *.log del *.log
cd ..

echo.
echo Installation des dependances...
echo.

:: Installer les dependances du frontend
echo Installation des dependances Node.js...
cd frontend
call npm install
if errorlevel 1 (
    echo ERREUR: Impossible d'installer les dependances Node.js
    pause
    exit /b 1
)
cd ..

:: Installer les dependances du backend
echo Installation des dependances Python...
cd backend
call pip install -r requirements.txt
if errorlevel 1 (
    echo ERREUR: Impossible d'installer les dependances Python
    pause
    exit /b 1
)
cd ..

echo.
echo ============================================================
echo INSTALLATION TERMINEE AVEC SUCCES!
echo ============================================================
echo.
echo Vous pouvez maintenant lancer l'application avec:
echo - demarrer_application.bat
echo - ou python start_dev.py
echo.
pause 