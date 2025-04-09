DEX_NETWORKS = {
    "avax": "avalanche",
    "sui-network": "sui",
    "xrp": "xrp"
}

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

            dex_network = DEX_NETWORKS.get(network, network)
            link = f"https://dexscreener.com/{dex_network}/{address}"

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


