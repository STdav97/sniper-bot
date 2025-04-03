import requests

def get_recent_tokens_sui():
    # Exemple fictif d'appel API pour récupérer tokens SUI récents
    url = "https://api.geckoterminal.com/api/v2/networks/sui-network/new_pools"
    res = requests.get(url)
    data = res.json()
    tokens = []
    for token in data['data'][:5]:
        tokens.append({
            'name': token['attributes']['name'],
            'link': f"https://www.geckoterminal.com/sui-network/pools/{token['attributes']['address']}"
        })
    return tokens

def get_recent_tokens_avax():
    # Exemple fictif d'appel API pour récupérer tokens AVAX récents
    url = "https://api.geckoterminal.com/api/v2/networks/avax/new_pools"
    res = requests.get(url)
    data = res.json()
    tokens = []
    for token in data['data'][:5]:
        tokens.append({
            'name': token['attributes']['name'],
            'link': f"https://www.geckoterminal.com/avax/pools/{token['attributes']['address']}"
        })
    return tokens
