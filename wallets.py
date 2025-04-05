import json
import os

WALLET_FILE = "wallets.json"

def load_wallets():
    if not os.path.exists(WALLET_FILE):
        return {}

    with open(WALLET_FILE, "r") as f:
        return json.load(f)

def save_wallets(wallets):
    with open(WALLET_FILE, "w") as f:
        json.dump(wallets, f, indent=4)

def set_wallet(user_id, network, address):
    wallets = load_wallets()
    user_id = str(user_id)
    if user_id not in wallets:
        wallets[user_id] = {}
    wallets[user_id][network] = address
    save_wallets(wallets)

def get_wallet(user_id, network):
    wallets = load_wallets()
    return wallets.get(str(user_id), {}).get(network)
