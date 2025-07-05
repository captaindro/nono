#!/usr/bin/env bash
set -eo pipefail

# Aller à la racine du projet
cd "$(dirname "$0")"

# Active l'environnement Python
if [ -d "newvenv" ]; then
  source newvenv/bin/activate
elif [ -d "venv" ]; then
  source venv/bin/activate
else
  echo "⚠️ Aucun venv trouvé (newvenv/venv)"
fi

# Installe les dépendances (utile si requirements ont changé)
pip install --upgrade pip
pip install -r requirements.txt

# Lance le bot NONO
exec python main.py
