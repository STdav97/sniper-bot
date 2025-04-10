from aiogram import Router, types
from aiogram.filters.command import Command
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
import json
from sniper_avax_testnet_v2 import run_avax_simulation
from web3 import Web3
import os

router = Router()

# ----------- CONFIG SMART CONTRACT ------------
PRIVATE_KEY = os.getenv("PRIVATE_KEY") or "TA_CLE_PRIVEE_TEST"
PUBLIC_WALLET = os.getenv("PUBLIC_WALLET") or "0xTON_WALLET"
CONTRACT_ADDRESS = os.getenv("CONTRACT_ADDRESS") or "0xTON_CONTRAT_DEPLOYE"
RPC_URL = "https://api.avax-test.network/ext/bc/C/rpc"
CHAIN_ID = 43113  # Fuji Testnet

CONTRACT_ABI = [
    {
        "inputs": [
            {"internalType": "address", "name": "tokenOut", "type": "address"}
        ],
        "name": "snipe",
        "outputs": [],
        "stateMutability": "payable",
        "type": "function"
    }
]

# ----------- /simulate_avax ------------
@router.message(Command("simulate_avax"))
async def simulate_avax_handler(message: types.Message):
    await message.answer("\ud83d\ude80 Lancement de la simulation AVAX testnet...")
    run_avax_simulation()

    try:
        with open("snipes_log.json", "r") as f:
            data = json.load(f)
            avax_tokens = [t for t in data if t["network"] == "AVAX"][-5:]

            for token in avax_tokens:
                text = (
                    f"\ud83d\udc8e Token : {token['name']} (AVAX)\n"
                    f"\ud83d\udcca Gain simul\u00e9 : +{token['gain']}%\n"
                    f"\ud83d\udd17 [Voir sur DexScreener]({token['link']})"
                )
                btn = InlineKeyboardMarkup(inline_keyboard=[
                    [InlineKeyboardButton(text="\ud83d\ude80 Voir sur DexScreener", url=token["link"])],
                    [InlineKeyboardButton(text=f"\ud83d\udd25 BUY NOW via Bot", callback_data=f"buy:{token['address']}")]
                ])
                await message.answer(text, parse_mode="Markdown", reply_markup=btn)

    except Exception as e:
        await message.answer(f"\u274c Erreur lecture fichier : {e}")

# ----------- /buy_now 0xAdresseToken ------------
@router.message(Command("buy_now"))
async def buy_now_handler(message: types.Message):
    try:
        token_address = message.text.split()[1]
        web3 = Web3(Web3.HTTPProvider(RPC_URL))

        contract = web3.eth.contract(
            address=Web3.to_checksum_address(CONTRACT_ADDRESS),
            abi=CONTRACT_ABI
        )

        nonce = web3.eth.get_transaction_count(PUBLIC_WALLET)
        txn = contract.functions.snipe(Web3.to_checksum_address(token_address)).build_transaction({
            'from': PUBLIC_WALLET,
            'value': web3.to_wei(0.01, 'ether'),
            'gas': 300000,
            'gasPrice': web3.to_wei('25', 'gwei'),
            'nonce': nonce,
            'chainId': CHAIN_ID
        })

        signed_txn = web3.eth.account.sign_transaction(txn, private_key=PRIVATE_KEY)
        tx_hash = web3.eth.send_raw_transaction(signed_txn.rawTransaction)
        tx_link = f"https://testnet.snowtrace.io/tx/{web3.to_hex(tx_hash)}"

        await message.answer(f"\u2705 Transaction envoy\u00e9e !\n\ud83d\udccb {tx_link}")

    except Exception as e:
        await message.answer(f"\u274c Erreur : {e}")

# ----------- /report ------------
@router.message(Command("report"))
async def report_handler(message: types.Message):
    try:
        with open("snipes_log.json", "r") as f:
            lines = f.readlines()

        if not lines:
            await message.answer("\u26a0\ufe0f Aucun snipe \u00e0 afficher pour l'instant.")
            return

        snipes = [json.loads(line) for line in lines]
        snipes = sorted(snipes, key=lambda x: x["gain_percent"], reverse=True)
        top_snipes = snipes[:5]

        response = "\ud83d\udcca *Top Snipes Testnet*\n\n"
        for s in top_snipes:
            response += (
                f"\u2728 *{s['token']}* ({s['network']})\n"
                f"\ud83d\udcca Gain : +{s['gain_percent']}%\n"
                f"\ud83d\udd5b {s['sniped_at'][11:19].replace('T', ' ')} UTC\n"
                f"\ud83d\udcc3 TX : `{s['tx_hash']}`\n\n"
            )

        await message.answer(response, parse_mode="Markdown")

    except Exception as e:
        await message.answer(f"\u274c Erreur lors du rapport : {e}")
