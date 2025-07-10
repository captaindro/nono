<<<<<<< HEAD
# Bot NONO

[...]

## Roadmap

### Phase 1 – Fondations (✅ Terminé)
- WebSocket Helius live  
- Wallet Solflare  
- Honeypot stub  
- Filtre liquidité Raydium  
- Swap basique via Jupiter  
- TP/SL statiques + auto-sell  
- Logs

### Phase 2 – Fonctionnalités avancées (✅ Terminé)
- Swap réel Jupiter  
- Vente automatique TP/SL  
- Honeypot réel  
- Recyclage des gains  
- TP/SL dynamiques selon volatilité

### Phase 3 – Dashboard & Monitoring (✅ Terminé)
- Dashboard web (FastAPI + WebSocket)  
- Boutons Start/Stop  
- Statistiques en temps réel  
- Paramètres à chaud (TP, SL, slippage, liquidité)

### Phase 4 – Stratégies intelligentes (EN COURS)
- 📈 Copy-Trading (à venir)  
- 🤖 Scoring IA : module de scoring token implanté (placeholder) ✅  
- 🔔 Notifications Discord/Telegram 🟡

## Usage

[...]
=======
# Projet NONO - Bot Sniping Solana Pump.fun

## Description
Bot Python async pour sniping automatique de tokens Solana via Pump.fun avec intégration Jupiter API.

## Structure
- `utils/trade.py` : logique principale d'analyse et achat
- `utils/jup_swap.py` : interaction API Jupiter et swap
- `wallets/wallet.py` : gestion wallet clé privée
- `test_handle.py` : tests simples de fonctionnalité

## Installation
```
pip install -r requirements.txt
```

## Usage
```
python test_handle.py
```

---

## Prochaines améliorations
- Récupération réelle et fiable du token info (Magic Eden / pump.fun)
- Construction complète des transactions swap selon Jupiter routes
- Gestion des erreurs réseaux et retry avancé
- Tests automatisés et monitoring
>>>>>>> 2553739 (Ajout de la config Railway et du workflow CI/CD)
