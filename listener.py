from flask import Flask, request
import json
from src.snipe import execute_snipe

app = Flask(__name__)

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json()
    if not data:
        return {"status": "no data"}, 400

    try:
        for tx in data.get("transactions", []):
            instructions = tx.get("events", {}).get("programs", [])
            for instr in instructions:
                if instr.get("programName") == "pumpfun" and instr.get("programId") == "6EF8rrecthR5Dkzon8Nwu78hRvfCKubJ14M5uBEwF6P":
                    accounts = instr.get("accounts", [])
                    if len(accounts) >= 3:
                        token_b = accounts[2].get("account")
                        print(f"[+] TokenB found: {token_b}")
                        execute_snipe(token_b)
        return {"status": "ok"}, 200
    except Exception as e:
        print(f"Error: {e}")
        return {"status": "error", "detail": str(e)}, 500
