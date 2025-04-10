import os
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters.command import Command
from dotenv import load_dotenv

from utils import get_recent_tokens_sui, get_recent_tokens_avax, get_recent_tokens_xrp, update_filters
from keep_alive import keep_alive
from storage import save_token
from report import router as report_router
from commands_simulation import router as simulation_router  # Pour /simulate_avax, /simulate_sui, /simulate_all
from wallets import set_wallet, get_wallet
from commands import router as commands_router
dp.include_router(commands_router)


load_dotenv()

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
bot = Bot(token=TOKEN)
dp = Dispatcher()

# ✅ Enregistre les routes externes
dp.include_router(report_router)
dp.include_router(simulation_router)

# ✅ Commande /start
@dp.message(Command("start"))
async def send_welcome(message: Message):
    await message.answer("🚀 Sniper Bot activé. Surveillance AVAX, SUI & XRP démarrée.")

# ✅ Commande /filter
@dp.message(Command("filter"))
async def set_filter(message: Message):
    try:
        parts = message.text.split()
        lp = volume = holders = None

        for p in parts[1:]:
            if "lp>" in p:
                lp = int(p.replace("lp>", ""))
            elif "volume>" in p:
                volume = int(p.replace("volume>", ""))
            elif "holders<" in p:
                holders = int(p.replace("holders<", ""))

        update_filters(lp, volume, holders)

        await message.answer(
            f"✅ Filtres mis à jour :\n"
            f"- LP ≥ {lp or 'inchangé'}\n"
            f"- Volume ≥ {volume or 'inchangé'}\n"
            f"- Holders < {holders or 'inchangé'}"
        )

    except Exception as e:
        await message.answer(
            "❌ Erreur dans la commande. Exemple correct :\n"
            "`/filter lp>2000 volume>1500 holders<400`",
            parse_mode="Markdown"
        )

# ✅ Commande /snip
@dp.message(Command("snip"))
async def send_tokens(message: Message):
    await message.answer("🔍 Je récupère les tokens récents...")

    sui_tokens = get_recent_tokens_sui()
    avax_tokens = get_recent_tokens_avax()
    xrp_tokens = get_recent_tokens_xrp()

    # SUI tokens
    for token in sui_tokens:
        save_token({
            "name": token['name'],
            "network": "SUI",
            "volume": token.get("volume", 0),
            "lp": token.get("liquidity", 0),
            "holders": token.get("holders", 0),
            "link": token['link']
        })
        btn = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="🚀 SNIPE", url=token['link'])]
        ])
        await message.answer(
            f"💎 Token : {token['name']} (SUI)\n🔗 [Voir sur GeckoTerminal]({token['link']})",
            parse_mode="Markdown",
            reply_markup=btn
        )

    # AVAX tokens
    for token in avax_tokens:
        save_token({
            "name": token['name'],
            "network": "AVAX",
            "volume": token.get("volume", 0),
            "lp": token.get("liquidity", 0),
            "holders": token.get("holders", 0),
            "link": token['link']
        })
        btn = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="🚀 SNIPE", url=token['link'])]
        ])
        await message.answer(
            f"💎 Token : {token['name']} (AVAX)\n🔗 [Voir sur GeckoTerminal]({token['link']})",
            parse_mode="Markdown",
            reply_markup=btn
        )

    # XRP tokens
    for token in xrp_tokens:
        save_token({
            "name": token['name'],
            "network": "XRP",
            "volume": token.get("volume", 0),
            "lp": token.get("liquidity", 0),
            "holders": token.get("holders", 0),
            "link": token['link']
        })
        btn = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="🚀 SNIPE", url=token['link'])]
        ])
        await message.answer(
            f"💎 Token : {token['name']} (XRP)\n🔗 [Voir sur GeckoTerminal]({token['link']})",
            parse_mode="Markdown",
            reply_markup=btn
        )

# ✅ Commande /faucet_sui
@dp.message(Command("faucet_sui"))
async def faucet_sui(message: Message):
    await message.answer(
        "💧 *SUI Testnet Faucet :*\n\n"
        "👉 https://faucet.testnet.sui.io/\n"
        "⚠️ Colle ton adresse SUI et clique sur *'Get SUI Tokens'*",
        parse_mode="Markdown"
    )

# ✅ Commande /set_wallet
@dp.message(Command("set_wallet"))
async def handle_set_wallet(message: Message):
    try:
        parts = message.text.split()
        if len(parts) != 3:
            raise ValueError("Format incorrect")
        
        network = parts[1].lower()
        address = parts[2]

        if network not in ["avax", "sui"]:
            await message.answer("❌ Réseau non reconnu. Utilise 'avax' ou 'sui'.")
            return
        
        set_wallet(message.from_user.id, network, address)
        await message.answer(f"✅ Wallet {network.upper()} enregistré avec succès !")

    except Exception:
        await message.answer("❌ Format incorrect.\nExemple : `/set_wallet avax 0xABC...`", parse_mode="Markdown")

# ✅ Commande /claim_all
@dp.message(Command("claim_all"))
async def claim_all(message: Message):
    user_id = message.from_user.id
    sui_address = get_wallet(user_id, "sui")
    avax_address = get_wallet(user_id, "avax")

    response = "💧 *Requêtes faucet :*\n\n"

    if sui_address:
        response += f"🔹 *SUI* → [Lien](https://faucet.testnet.sui.io/) pour `{sui_address}`\n"
    else:
        response += "🔹 *SUI* → ❌ Adresse manquante\n"

    if avax_address:
        response += f"🔹 *AVAX* → [Lien](https://faucet.avax.network/) pour `{avax_address}`\n"
    else:
        response += "🔹 *AVAX* → ❌ Adresse manquante\n"

    await message.answer(response, parse_mode="Markdown")


# ✅ Commande /faucet_avax
@dp.message(Command("faucet_avax"))
async def faucet_avax(message: Message):
    await message.answer(
        "💧 *AVAX Fuji Testnet Faucet :*\n\n"
        "👉 https://faucet.avax.network/\n"
        "🔗 Sélectionne *Fuji C-Chain*, colle ton adresse MetaMask, puis clique sur *'Request AVAX'*",
        parse_mode="Markdown"
    )

# ✅ Lancer le bot
async def main():
    keep_alive()
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())



