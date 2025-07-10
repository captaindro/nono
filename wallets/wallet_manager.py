# wallets/wallet_manager.py

import os
import random
import json
from solders.keypair import Keypair
from config.settings import settings

def list_wallet_paths():
    folder = settings.wallet_folder
    return [
        os.path.join(folder, f)
        for f in os.listdir(folder)
        if f.endswith(".json")
    ]

def get_random_wallet_path() -> str:
    paths = list_wallet_paths()
    return random.choice(paths)

def load_keypair_from_file(path: str) -> Keypair:
    with open(path, "r") as f:
        secret = json.load(f)
    return Keypair.from_bytes(bytes(secret))

def get_random_wallet() -> Keypair:
    """Retourne un wallet Keypair aléatoire à partir du dossier wallets/"""
    path = get_random_wallet_path()
    return load_keypair_from_file(path)

def get_wallet_pubkey_from_path(path: str) -> str:
    keypair = load_keypair_from_file(path)
    return str(keypair.pubkey())
