import requests
import time

# Adresses tokens et pools
USDC = "0xFF970A61A04b1cA14834A43f5dE4533eBDDB5CC8"
WETH = "0x82af49447d8a07e3bd95bd0d56f35241523fbab1"

# Adresses API (Uniswap V3 et SushiSwap sur Arbitrum)
uniswap_api = "https://api.thegraph.com/subgraphs/name/ianlapham/arbitrum-dev"
sushiswap_api = "https://api.thegraph.com/subgraphs/name/sushiswap/arbitrum-exchange"

def get_price(pool_api, tokenA, tokenB):
    query = """
    {
      pairs(where: {token0: "%s", token1: "%s"}) {
        token0Price
        token1Price
      }
    }
    """ % (tokenA.lower(), tokenB.lower())
    resp = requests.post(pool_api, json={'query': query})
    data = resp.json()
    pairs = data['data']['pairs']
    if not pairs:
        return None, None
    return float(pairs[0]['token0Price']), float(pairs[0]['token1Price'])

while True:
    try:
        # Prix Uniswap
        uni0, uni1 = get_price(uniswap_api, USDC, WETH)
        # Prix Sushiswap
        sushi0, sushi1 = get_price(sushiswap_api, USDC, WETH)

        if None in [uni0, uni1, sushi0, sushi1]:
            print("Pool non trouvé")
        else:
            print(f"Uniswap USDC/ETH: {uni0:.6f} USDC/ETH | SushiSwap USDC/ETH: {sushi0:.6f} USDC/ETH")
            # Condition d'arbitrage profitable
            if uni0 > sushi0 * 1.002:  # 0.2% de profit minimum (à ajuster selon frais)
                print("🚨 OPPORTUNITÉ ARBITRAGE: Vendre sur Uniswap, Acheter sur SushiSwap !")
                # Tu peux ici exécuter ton smart contract automatiquement
            elif sushi0 > uni0 * 1.002:
                print("🚨 OPPORTUNITÉ ARBITRAGE: Vendre sur SushiSwap, Acheter sur Uniswap !")
                # Exécuter ton smart contract automatiquement
            else:
                print("Pas d'opportunité pour l'instant.")

    except Exception as e:
        print("Erreur:", e)

    time.sleep(5)  # Vérifie toutes les 5 secondes
    # Script de surveillance des opportunités d'arbitrage entre Uniswap V3 et Sushiswap sur Arbitrum

