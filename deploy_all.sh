#!/usr/bin/env bash
set -euo pipefail

# 1. Crée les dossiers nécessaires
mkdir -p .railway dashboard .github/workflows

# 2. Écrit les fichiers

# .env
cat > .env << 'EOF'
########################################
# Variables d’environnement pour le Bot NONO
########################################

# Choisissez l’environnement : 'mainnet' ou 'devnet'
ENVIRONMENT=mainnet

# Clé API Helius (identique pour mainnet et devnet)
HEL_API_KEY=75c7c75c-0230-482e-af0e-f2860324e474

# Endpoints Mainnet
RPC_URL_MAINNET=https://mainnet.helius-rpc.com/?api-key=${HEL_API_KEY}
WS_URL_MAINNET=wss://mainnet.helius-rpc.com/?api-key=${HEL_API_KEY}

# Endpoints Devnet
RPC_URL_DEVNET=https://devnet.helius-rpc.com/?api-key=${HEL_API_KEY}
WS_URL_DEVNET=wss://devnet.helius-rpc.com/?api-key=${HEL_API_KEY}

# Chemin vers le wallet JSON (clé privée)
WALLET_PATH=wallets/wallet.json

# Clé publique du wallet (pour simulation honeypot)
YOUR_PUBLIC_KEY=4ACfpUFoaSD9bfPdeu6DBt89gB6ENTeHBXCAi87NhDEE

# Token Railway CLI (pour CI/CD et start.sh)
RAILWAY_TOKEN=fce25eff-ccef-418b-a9bd-e891a1a4f70b
EOF

# requirements.txt
cat > requirements.txt << 'EOF'
python-dotenv==1.0.0
ruamel.yaml==0.17.21
websockets==10.4
requests==2.31.0
solana==0.22.0
pytest==7.4.0
EOF

# pytest.ini
cat > pytest.ini << 'EOF'
[pytest]
testpaths = tests
pythonpath = .
EOF

# setup.py
cat > setup.py << 'EOF'
from setuptools import setup, find_packages

setup(
    name="nono",
    version="0.1.0",
    packages=find_packages(),
    include_package_data=True,
)
EOF

# start.sh
cat > start.sh << 'EOF'
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
EOF

# railway.json
cat > railway.json << 'EOF'
{
  "$schema": "https://railway.com/railway.schema.json",
  "projectId": "d594651f-0024-4331-a738-6ef98b1a3405",
  "projectToken": "fce25eff-ccef-418b-a9bd-e891a1a4f70b",
  "build": {
    "builder": "NIXPACKS"
  },
  "deploy": {
    "runtime": "V2",
    "numReplicas": 1,
    "sleepApplication": false,
    "multiRegionConfig": {
      "europe-west4-drams3a": {
        "numReplicas": 1
      }
    },
    "restartPolicyType": "ON_FAILURE",
    "restartPolicyMaxRetries": 10,
    "startCommand": "./start.sh"
  }
}
EOF

# .railway/overrides.json
cat > .railway/overrides.json << 'EOF'
{
  "projectId": "d594651f-0024-4331-a738-6ef98b1a3405",
  "environment": "production",
  "service": "nono"
}
EOF

# GitHub Actions workflow
cat > .github/workflows/deploy.yml << 'EOF'
name: CI & Deploy to Railway

on:
  push:
    branches:
      - main

jobs:
  test:
    name: 🧪 Run Tests
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - uses: actions/setup-python@v4
        with:
          python-version: '3.12'

      - name: Install dependencies & package
        run: |
          pip install --upgrade pip
          pip install -r requirements.txt
          pip install -e .

      - name: Expose project root to PYTHONPATH
        run: echo "PYTHONPATH=${{ github.workspace }}" >> $GITHUB_ENV

      - name: Run pytest
        run: pytest -q

  deploy:
    name: 🚀 Deploy to Railway
    needs: test
    runs-on: ubuntu-latest
    env:
      RAILWAY_TOKEN: ${{ secrets.RAILWAY_TOKEN }}

    steps:
      - uses: actions/checkout@v3

      - name: Install Railway CLI
        run: curl -sSL https://railway.app/install.sh | sh

      - name: Deploy service "nono"
        run: railway up --service nono
        env:
          RAILWAY_TOKEN: ${{ secrets.RAILWAY_TOKEN }}
EOF

# Dashboard backend
cat > dashboard/app.py << 'EOF'
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
import asyncio, os, subprocess

app = FastAPI()
bot_process = None
clients: list[WebSocket] = []

with open(os.path.join(os.path.dirname(__file__), "index.html")) as f:
    html = f.read()

@app.get("/")
async def get_dashboard():
    return HTMLResponse(html)

@app.websocket("/ws")
async def ws_endpoint(ws: WebSocket):
    await ws.accept()
    clients.append(ws)
    try:
        while True:
            await asyncio.sleep(1)
    except WebSocketDisconnect:
        clients.remove(ws)

async def broadcast(msg: str):
    for ws in clients:
        await ws.send_text(msg)

@app.post("/bot/start")
async def start_bot():
    global bot_process
    if bot_process and bot_process.poll() is None:
        return {"status": "already_running"}
    bot_process = subprocess.Popen(["python", "../main.py"], cwd=os.getcwd())
    await broadcast("BOT_STARTED")
    return {"status": "started"}

@app.post("/bot/stop")
async def stop_bot():
    global bot_process
    if not bot_process or bot_process.poll() is not None:
        return {"status": "not_running"}
    bot_process.terminate()
    await broadcast("BOT_STOPPED")
    return {"status": "stopped"}
EOF

# Dashboard frontend
cat > dashboard/index.html << 'EOF'
<!DOCTYPE html>
<html lang="fr">
<head>
  <meta charset="utf-8">
  <title>Dashboard Bot NONO</title>
  <meta name="viewport" content="width=device-width, initial-scale=1">

  <style>
    * { margin: 0; padding: 0; box-sizing: border-box; }
    body {
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
      background-color: #f5f5f7; color: #1d1d1f;
      padding: 2rem; display: flex; flex-direction: column; align-items: center;
    }
    h1 { margin-bottom: 1rem; font-size: 2rem; font-weight: 600; }
    .controls { display: flex; gap: 1rem; margin-bottom: 2rem; }
    button {
      padding: 0.75rem 1.5rem; border: none; border-radius: 0.5rem;
      background-color: #0071e3; color: #fff; font-size: 1rem; cursor: pointer;
      transition: background-color 0.2s;
    }
    button:hover { background-color: #005bb5; }
    button:disabled { background-color: #c7c7cc; cursor: default; }
    #log {
      width: 100%; max-width: 800px; height: 400px; background: #fff;
      border-radius: 0.75rem; box-shadow: 0 4px 12px rgba(0,0,0,0.05);
      overflow-y: auto; padding: 1rem; font-family: Menlo, monospace; font-size: 0.9rem;
      color: #2c2c2e;
    }
    #log p { margin-bottom: 0.5rem; }
  </style>
</head>
<body>
  <h1>Bot NONO Dashboard</h1>
  <div class="controls">
    <button id="startBtn" onclick="startBot()">Démarrer le bot</button>
    <button id="stopBtn" onclick="stopBot()" disabled>Arrêter le bot</button>
  </div>
  <div id="log"></div>
  <script>
    const logEl = document.getElementById("log"),
          startBtn = document.getElementById("startBtn"),
          stopBtn  = document.getElementById("stopBtn");
    const ws = new WebSocket((location.protocol==='https:'?'wss://':'ws://')+location.host+'/ws');
    ws.onopen = ()=>append('🔌 WebSocket connecté');
    ws.onclose= ()=>append('⚠️ WebSocket déconnecté');
    ws.onmessage=evt=>append(evt.data);
    function append(t){ const p=document.createElement('p'); p.textContent=t; logEl.appendChild(p); logEl.scrollTop=logEl.scrollHeight; }
    async function startBot(){
      startBtn.disabled=true; append('→ Envoi START…');
      let r=await fetch('/bot/start',{method:'POST'}),d=await r.json();
      append(`✅ Start: ${d.status}`); if(d.status==='started')stopBtn.disabled=false; else startBtn.disabled=false;
    }
    async function stopBot(){
      stopBtn.disabled=true; append('→ Envoi STOP…');
      let r=await fetch('/bot/stop',{method:'POST'}),d=await r.json();
      append(`✅ Stop: ${d.status}`); if(d.status==='stopped')startBtn.disabled=false; else stopBtn.disabled=false;
    }
  </script>
</body>
</html>
EOF

# Dashboard requirements
cat > dashboard/requirements.txt << 'EOF'
fastapi==0.95.0
uvicorn==0.22.0
EOF

# 3. Normalise LF
find . -type f \( -name "*.sh" -o -name "*.json" -o -name "*.yml" -o -name "*.yaml" -o -name "*.py" -o -name "*.html" \) -exec sed -i 's/\r$//' {} +

# 4. Rends start.sh exécutable
chmod +x start.sh

# 5. Git add, commit & push
git add .
git commit -m "Deploy all Phase 3 files: env, CI, dashboard, overrides"
git push origin main