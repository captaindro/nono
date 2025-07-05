#!/usr/bin/env bash
set -eo pipefail

# Vérifie qu'un message de commit est passé
if [ -z "$1" ]; then
  echo "Usage: ./deploy_all.sh \"Message de commit\""
  exit 1
fi
COMMIT_MSG="$1"

# 1) Ajout, commit, push sur GitHub
git add .
git commit -m "$COMMIT_MSG"
git push origin main

# 2) Login Railway (silencieux si déjà loggé)
railway login || true

# 3) Lier le projet (une seule fois, ignore si déjà lié)
railway link --project "$RAILWAY_PROJECT_ID" --yes || true

# 4) Déployer le service NONO
echo "🚀 Deploying 'nono' service..."
railway up --service nono

# 5) Déployer le dashboard (si vous avez un service séparé nommé 'nono-dashboard')
echo "🚀 Deploying 'nono-dashboard' service..."
railway up --service nono-dashboard

echo "✅ Déploiement complet terminé!"
