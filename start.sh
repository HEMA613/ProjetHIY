#!/bin/bash
# Script de démarrage du Backend et Frontend

echo ""
echo "==================================="
echo "  Vacation Manager - Démarrage"
echo "==================================="
echo ""

# Vérifier Python
if ! command -v python3 &> /dev/null; then
    echo "ERREUR: Python n'est pas installé"
    exit 1
fi

echo "[1/4] Installation des dépendances backend..."
cd backend
pip install -r requirements.txt -q
if [ $? -ne 0 ]; then
    echo "ERREUR: Impossible d'installer les dépendances backend"
    exit 1
fi

echo "[2/4] Installation des dépendances frontend..."
cd ../frontend
pip install -r requirements.txt -q
if [ $? -ne 0 ]; then
    echo "ERREUR: Impossible d'installer les dépendances frontend"
    exit 1
fi

echo "[3/4] Démarrage du Backend (API sur port 5000)..."
cd ../backend
python3 api.py &
BACKEND_PID=$!
echo ""
echo "Attendez 2 secondes pour que l'API démarre..."
sleep 2

echo "[4/4] Démarrage du Frontend..."
cd ../frontend
python3 main_connected.py

# Arrêter le backend en même temps que le frontend
kill $BACKEND_PID 2>/dev/null

echo ""
echo "==================================="
echo "   Application arrêtée"
echo "==================================="
