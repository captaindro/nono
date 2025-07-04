#!/bin/bash

if [ -z "$1" ]; then
  echo "❌ Merci de fournir un message de commit."
  echo "Usage : ./deploy.sh \"feat: ajout de heartbeat\""
  exit 1
fi

echo "🚀 Déploiement en cours..."
git add .
git commit -m "$1"
git push origin master
echo "✅ Code poussé sur GitHub. Railway va maintenant déployer automatiquement."
