# start.sh
#!/usr/bin/env bash
set -euo pipefail

# 1️⃣ Active le virtualenv
source newvenv/bin/activate

# 2️⃣ Charge les variables d’environnement depuis .env
set -o allexport
source .env
set +o allexport

# 3️⃣ Affiche les logs du service 'nono' (Railway CLI utilise RAILWAY_TOKEN sans login)
railway logs --service nono
