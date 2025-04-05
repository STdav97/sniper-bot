import os
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters.command import Command
from dotenv import load_dotenv
from utils import get_recent_tokens_sui, get_recent_tokens_avax, get_recent_tokens_xrp, update_filters
from keep_alive import keep_alive
from storage import save_token

# ✅ Import des routes de commandes externes
from report import router as report_router
from commands_simulation import router as simulation_router  # Pour /simulate_avax et /simulate_sui

load_dotenv()

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
bot = Bot(token=TOKEN)
dp = Dispatcher()

# ✅ Enregistrement des routes
dp.include_router(report_router)
dp.include_router(simulation_router)

load_dotenv()

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
bot = Bot(token=TOKEN)
dp = Dispatcher()

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

# ✅ Lancer le bot
async def main():
    keep_alive()
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())


