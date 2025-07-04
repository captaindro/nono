from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
import asyncio
import os
import subprocess

app = FastAPI()

# Stocke l’état du bot et les websockets clients
bot_process = None
clients: list[WebSocket] = []

# Page HTML embarquée
with open(os.path.join(os.path.dirname(__file__), "index.html"), "r") as f:
    html = f.read()

@app.get("/")
async def get_dashboard():
    return HTMLResponse(html)

@app.websocket("/ws")
async def websocket_endpoint(ws: WebSocket):
    await ws.accept()
    clients.append(ws)
    try:
        while True:
            await asyncio.sleep(1)
    except WebSocketDisconnect:
        clients.remove(ws)

async def broadcast(message: str):
    for ws in clients:
        await ws.send_text(message)

@app.post("/bot/start")
async def start_bot():
    global bot_process
    if bot_process and bot_process.poll() is None:
        return {"status": "already_running"}
    # Lancement du bot en subprocess
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
