from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Body
from fastapi.responses import HTMLResponse, JSONResponse
import asyncio, os, subprocess
from pydantic import BaseModel

app = FastAPI()
bot_process = None
clients: list[WebSocket] = []

# Stats in-memory
stats = {
    "total_snipes": 0,
    "successful_snipes": 0,
    "failed_snipes": 0,
    "total_pnl": 0.0
}

# Dynamic parameters (default values)
params = {
    "take_profit_multiplier": 1.1,
    "stop_loss_multiplier": 0.8,
    "slippage_bps": 50,
    "liquidity_threshold_sol": 0.5
}

with open(os.path.join(os.path.dirname(__file__), "index.html")) as f:
    html = f.read()

class ParamsUpdate(BaseModel):
    take_profit_multiplier: float
    stop_loss_multiplier: float
    slippage_bps: int
    liquidity_threshold_sol: float

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
        try:
            await ws.send_text(msg)
        except:
            pass

@app.post("/bot/start")
async def start_bot():
    global bot_process
    if bot_process and bot_process.poll() is None:
        return {"status": "already_running"}
    bot_process = subprocess.Popen(
        ["python", "main.py"], cwd=os.getcwd(),
        env={**os.environ, **{k: str(v) for k,v in params.items()}}
    )
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

@app.get("/stats")
async def get_stats():
    return JSONResponse(stats)

@app.post("/stats/event")
async def add_event(event: dict = Body(...)):
    # event: {"success": bool, "pnl": float}
    stats["total_snipes"] += 1
    if event.get("success"):
        stats["successful_snipes"] += 1
    else:
        stats["failed_snipes"] += 1
    stats["total_pnl"] += float(event.get("pnl", 0.0))
    await broadcast(f"STATS {stats}")
    return {"status": "ok"}

@app.get("/params")
async def get_params():
    return JSONResponse(params)

@app.post("/params")
async def update_params(update: ParamsUpdate):
    params.update(update.dict())
    await broadcast(f"PARAMS_UPDATED {params}")
    return {"status": "ok", "params": params}
