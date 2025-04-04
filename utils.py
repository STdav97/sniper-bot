import requests

# Filtres dynamiques
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

def get_recent_tokens(network):
    try:
        url = f"https://api.geckoterminal.com/api/v2/networks/{network}/new_pools"
        res = requests.get(url, timeout=10)
        data = res.json()
    except:
        return []

    tokens = []
    for token in data.get("data", []):
        try:
            attr = token['attributes']
            name = attr['name']
            address = attr['address']
            link = f"https://www.geckoterminal.com/{network}/pools/{address}"
            volume = float(attr.get("volume_usd", {}).get("h24", 0))
            liquidity = float(attr.get("reserve_in_usd", 0))
            holders = int(attr.get("pool_token_holders", 0))

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

def get_recent_tokens_sui():
    return get_recent_tokens("sui-network")

def get_recent_tokens_avax():
    return get_recent_tokens("avax")

def get_recent_tokens_xrp():
    return get_recent_tokens("xrp")

