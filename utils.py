import requests

# 🔧 Filtres modifiables dynamiquement via Telegram
FILTERS = {
    "lp_min": 3000,
    "volume_min": 1000,
    "holders_max": 500
}

def update_filters(lp=None, volume=None, holders=None):
    if lp is not None:
        FILTERS["lp_min"] = lp
    if volume is not None:
        FILTERS["volume_min"] = volume
    if holders is not None:
        FILTERS["holders_max"] = holders

def get_recent_tokens_sui():
    url = "https://api.geckoterminal.com/api/v2/networks/sui/new_pools"
    res = requests.get(url)
    data = res.json()

    tokens = []
    for token in data["data"]:
        try:
            name = token['attributes']['name']
            link = f"https://www.geckoterminal.com/sui-network/pools/{token['attributes']['address']}"
            volume = float(token["attributes"]["volume_usd"]["h24"] or 0)
            liquidity = float(token["attributes"]["reserve_in_usd"] or 0)
            holders = int(token["attributes"]["pool_token_holders"] or 0)

            if (
                volume >= FILTERS["volume_min"] and
                liquidity >= FILTERS["lp_min"] and
                holders < FILTERS["holders_max"]
            ):
                tokens.append({
                    "name": name,
                    "link": link,
                    "volume": volume,
                    "liquidity": liquidity,
                    "holders": holders
                })

            if len(tokens) >= 5:
                break
        except:
            continue

    return tokens

def get_recent_tokens_avax():
    url = "https://api.geckoterminal.com/api/v2/networks/avax/new_pools"
    res = requests.get(url)
    data = res.json()

    tokens = []
    for token in data["data"]:
        try:
            name = token['attributes']['name']
            link = f"https://www.geckoterminal.com/avax/pools/{token['attributes']['address']}"
            volume = float(token["attributes"]["volume_usd"]["h24"] or 0)
            liquidity = float(token["attributes"]["reserve_in_usd"] or 0)
            holders = int(token["attributes"]["pool_token_holders"] or 0)

            if (
                volume >= FILTERS["volume_min"] and
                liquidity >= FILTERS["lp_min"] and
                holders < FILTERS["holders_max"]
            ):
                tokens.append({
                    "name": name,
                    "link": link,
                    "volume": volume,
                    "liquidity": liquidity,
                    "holders": holders
                })

            if len(tokens) >= 5:
                break
        except:
            continue

    return tokens

