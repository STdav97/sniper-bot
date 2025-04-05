import time
import json
import random
from datetime import datetime
import uuid

# Génère un faux token testnet aléatoire
def generate_test_token():
    fake_names = ["TestX", "AlphaCoin", "DevToken", "GhostSwap", "ZeroDex"]
    networks = ["SUI", "AVAX", "XRP"]
    name = random.choice(fake_names)
    network = random.choice(networks)
    return {
        "id": str(uuid.uuid4())[:8],
        "name": name,
        "network": network,
        "volume": random.randint(1000, 100000),
        "liquidity": random.randint(500, 50000),
        "holders": random.randint(10, 500),
        "link": f"https://geckoterminal.com/{network.lower()}/pools/{uuid.uuid4().hex[:16]}"
    }

# Simule le sniping d'un token selon les filtres
def simulate_snipe(token):
    print(f"\n🛰️ Token détecté : {token['name']} ({token['network']})")
    print(f"🔗 {token['link']}")
    print(f"📊 Volume: ${token['volume']} | LP: ${token['liquidity']} | Holders: {token['holders']}")
    time.sleep(1)

    if token["volume"] > 1500 and token["liquidity"] > 2000 and token["holders"] < 400:
        print("✅ Critères VALIDÉS. Achat simulé.")
        token["sniped_at"] = datetime.utcnow().isoformat()
        with open("sniped_testnet.json", "a") as f:
            f.write(json.dumps(token) + "\n")
        print("💾 Token enregistré dans sniped_testnet.json")
    else:
        print("⛔ Critères NON validés. Token ignoré.")

# Lance la simulation sur 5 tokens aléatoires
if __name__ == "__main__":
    print("🎯 Simulation de sniping testnet commencée...\n")
    for _ in range(5):
        token = generate_test_token()
        simulate_snipe(token)
        time.sleep(2)
    print("\n✅ Simulation terminée.")
