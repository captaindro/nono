# main.py
import os
import asyncio
import logging
from dotenv import load_dotenv
from ruamel.yaml import YAML
import websockets

from utils.parser      import parse_msg
from utils.liquidity   import get_liquidity
from utils.honeypot    import is_honeypot
from utils.jupiter     import execute_swap
from utils.tp_sl       import compute_tp_sl
from utils.monitor    import monitor_position
from utils.reinvest    import get_reinvest_amount

# 1. Charger .env et config.yaml
load_dotenv()
env = os.getenv('ENVIRONMENT', 'mainnet').lower()

# 2. Sélection dynamique des endpoints
RPC_URL = os.getenv(f'RPC_URL_{env.upper()}')
WS_URL  = os.getenv(f'WS_URL_{env.upper()}')
API_KEY = os.getenv('HEL_API_KEY')

yaml = YAML(typ='safe')
with open('config.yaml', 'r') as f:
    settings = yaml.load(f)

# 3. Injecter les variables actives dans settings
settings.update({
    'rpc_url':     RPC_URL,
    'ws_url':      WS_URL,
    'api_key':     API_KEY,
    'wallet_path': os.getenv('WALLET_PATH'),
    'public_key':  os.getenv('YOUR_PUBLIC_KEY'),
})

async def websocket_listener(settings):
    headers = {'Authorization': f'Bearer {settings["api_key"]}'}
    logging.info(f"▶️ Connexion WS ({env}) à {settings['ws_url']}")
    async with websockets.connect(settings['ws_url'], extra_headers=headers) as ws:
        async for msg in ws:
            data = parse_msg(msg)
            token = data.get('mint')
            if not token:
                continue

            # 1️⃣ Vérif Liquidité
            liq = get_liquidity(token)
            if liq < settings['liquidity_threshold_sol']:
                continue

            # 2️⃣ Calcul montant à snip­er (avec réinvest si activé)
            base_amt = settings['jupiter']['swap_amount']
            swap_amt = get_reinvest_amount(base_amt, settings)

            # 3️⃣ Honeypot
            if settings['honeypot_check'] and is_honeypot(
                token,
                amount=swap_amt,
                slippage_bps=settings['jupiter']['slippage_bps'],
                user_public_key=settings['public_key']
            ):
                continue

            # 4️⃣ Achat via Jupiter
            sig_in, entry_price = execute_swap(
                input_mint="So11111111111111111111111111111111111111112",
                output_mint=token,
                amount=swap_amt,
                slippage_bps=settings['jupiter']['slippage_bps']
            )

            # 5️⃣ TP/SL + auto-sell
            tp_price, sl_price = compute_tp_sl(entry_price, settings)
            await monitor_position(
                sig_in=sig_in,
                tp=tp_price,
                sl=sl_price,
                timeout_seconds=settings['jupiter']['timeout_seconds'],
                token_mint=token,
                amount=swap_amt,
                settings=settings
            )

async def main():
    logging.basicConfig(
        level=logging.INFO,
        format='[%(asctime)s] %(levelname)s %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    logging.info(f"🚀 Démarrage du bot NONO en environnement {env.upper()}")
    await websocket_listener(settings)

if __name__ == "__main__":
    asyncio.run(main())
