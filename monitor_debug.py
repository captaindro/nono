import asyncio
import json
import websockets
import os

HELIUS_KEY = os.getenv("HELIUS_KEY", "75c7c75c-0230-482e-af0e-f2860324e474")
PUMP_FUN_PROGRAM = "GvHe5itKXzkVbM57pjgEfYy3sLBZLkzFEypPjWMCt1J7"

async def monitor_debug():
    uri = f"wss://rpc.helius.xyz/?api-key={HELIUS_KEY}"
    async with websockets.connect(uri) as ws:
        sub_msg = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "programSubscribe",
            "params": [
                PUMP_FUN_PROGRAM,
                {"encoding": "jsonParsed", "commitment": "processed"}
            ]
        }
        await ws.send(json.dumps(sub_msg))
        print("[🟢] WebSocket connecté à Helius. Analyse en cours des messages entrants...")

        while True:
            try:
                msg = await ws.recv()
                print("\n==========================")
                print("[📩] Nouveau message reçu :")
                print(msg)
                print("==========================")

                # Décode et affiche sous forme dict si possible
                try:
                    response = json.loads(msg)
                    acc_data = response.get("params", {}).get("result", {})
                    account = acc_data.get("account", {})
                    print("[🧠] Résumé parsed:")
                    print(f" - pubkey: {acc_data.get('pubkey')}")
                    print(f" - owner:  {account.get('owner')}")
                    print(f" - lamports: {account.get('lamports')}\n")
                except Exception as inner:
                    print(f"[⚠️] Erreur parsing JSON structuré: {inner}")
            except Exception as outer:
                print(f"[❌] Erreur réception WebSocket : {outer}")

if __name__ == "__main__":
    asyncio.run(monitor_debug())
