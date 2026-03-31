@echo off
REM Script de démarrage du Backend et Frontend

echo.
echo ===================================
echo   Vacation Manager - Démarrage
echo ===================================
echo.

REM Vérifier Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERREUR: Python n'est pas installé
    exit /b 1
)

echo [1/4] Installation des dépendances backend...
cd backend
pip install -r requirements.txt -q
if %errorlevel% neq 0 (
    echo ERREUR: Impossible d'installer les dépendances backend
    exit /b 1
)

echo [2/4] Installation des dépendances frontend...
cd ..\frontend
pip install -r requirements.txt -q
if %errorlevel% neq 0 (
    echo ERREUR: Impossible d'installer les dépendances frontend
    exit /b 1
)

echo [3/4] Démarrage du Backend (API sur port 5000)...
cd ..\backend
start /b python api.py
echo.
echo Attendez 2 secondes pour que l'API démarre...
timeout /t 2 /nobreak

echo [4/4] Démarrage du Frontend...
cd ..\frontend
start python main_connected.py

echo.
echo ===================================
echo   Application démarrée !
echo ===================================
echo.
echo Frontend: http://localhost (Tkinter)
echo Backend: http://localhost:5000/api
echo Health Check: http://localhost:5000/api/health
echo.
echo Pour arrêter:
echo - Fermer les fenêtres de l'application
echo - Ou utiliser Ctrl+C dans les terminaux
echo.
pause
