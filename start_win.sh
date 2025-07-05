#!/usr/bin/env bash
set -euo pipefail

# Active le virtualenv
source newvenv/bin/activate

# Exporte toutes les variables du .env
set -o allexport
source .env
set +o allexport

# Login Railway non-interactif
railway login --apiKey "$RAILWAY_TOKEN"

# Suis les logs du service 'nono'
railway logs --service nono
