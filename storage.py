import json
from datetime import datetime
import os

DB_FILE = "sniped_tokens.json"

def save_token(token_data):
    if not os.path.exists(DB_FILE):
        with open(DB_FILE, "w") as f:
            json.dump([], f)

    with open(DB_FILE, "r") as f:
        existing = json.load(f)

    # Évite les doublons
    if not any(t["link"] == token_data["link"] for t in existing):
        token_data["timestamp"] = datetime.now().isoformat()
        existing.append(token_data)

        with open(DB_FILE, "w") as f:
            json.dump(existing, f, indent=2)

def load_sniped_tokens():
    try:
        with open(DB_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def get_top_tokens(limit=5):
    tokens = load_sniped_tokens()

    def score(t):
        # Score = volume + LP - pression des holders
        return round((t["volume"] / 1000) + (t["liquidity"] / 1000) - (t["holders"] / 200), 2)

    for t in tokens:
        t["score"] = score(t)

    tokens = sorted(tokens, key=lambda x: x["score"], reverse=True)
    return tokens[:limit]
