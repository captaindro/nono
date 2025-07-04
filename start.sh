#!/usr/bin/env bash
set -euo pipefail

# 1️⃣ Active le virtualenv
source newvenv/bin/activate

# 2️⃣ Charge les variables depuis .env
set -o allexport
source .env
set +o allexport

# 3️⃣ Exporte le token pour la CLI Railway
export RAILWAY_TOKEN

# 4️⃣ Déploie le service 'nono' non-interactivement
railway up --service nono
