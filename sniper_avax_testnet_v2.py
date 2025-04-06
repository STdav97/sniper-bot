import random
import time
import json
from storage import save_token

# 👇 Fusion automatique dans snipes_log.json
def merge_to_global_log(token_data):
    try:
        with open("snipes_log.json", "r") as f:
            existing = json.load(f)
    except FileNotFoundError:
        existing = []

    existing.append(token_data)
    with open("snipes_log.json", "w") as f:
        json.dump(existing, f, indent=2)

# ✅ Simule des tokens récents sur AVAX testnet avec données dynamiques
def simulate_token_data_avax():
    fake_tokens = []
    for i in range(5):
        name = f"TKN{i+1}-AVAX"
        volume = random.randint(500, 5000)
        lp = random.randint(1000, 10000)
        holders = random.randint(50, 500)
        gain = round(random.uniform(1.1, 5.0), 2)

        fake_tokens.append({
            "name": name,
            "volume": volume,
            "liquidity": lp,
            "holders": holders,
            "gain": gain,
            "link": f"https://www.geckoterminal.com/avax/pools/{name.lower()}"
        })
    return fake_tokens

# ✅ Simulation complète avec fusion des logs
def run_avax_simulation():
    tokens = simulate_token_data_avax()
    for token in tokens:
        print(f"[AVAX TESTNET] Simulated token: {token['name']}, Gain: x{token['gain']}")
        
        save_token({
            "name": token["name"],
            "network": "AVAX",
            "volume": token["volume"],
            "lp": token["liquidity"],
            "holders": token["holders"],
            "gain": token["gain"],
            "link": token["link"]
        })

        merge_to_global_log({
            "name": token["name"],
            "network": "AVAX",
            "volume": token["volume"],
            "lp": token["liquidity"],
            "holders": token["holders"],
            "gain": token["gain"],
            "link": token["link"]
        })

        time.sleep(0.5)

# Facultatif : test direct
if __name__ == "__main__":
    run_avax_simulation()

