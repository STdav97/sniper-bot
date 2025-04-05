import os
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters.command import Command
from dotenv import load_dotenv
from utils import get_recent_tokens_sui, get_recent_tokens_avax, get_recent_tokens_xrp, update_filters
from keep_alive import keep_alive

load_dotenv()

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
bot = Bot(token=TOKEN)
dp = Dispatcher()

# ✅ Commande /start
@dp.message(Command("start"))
async def send_welcome(message: Message):
    await message.answer("🚀 Sniper Bot activé. Surveillance AVAX & SUI démarrée.")

# ✅ Commande /filter
import requests
@dp.message(Command("filter"))
async def set_filter(message: Message):
    try:

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
    url = f"https://api.geckoterminal.com/api/v2/networks/{network}/new_pools"
    res = requests.get(url)
    data = res.json()

    tokens = []
    for token in data.get("data", []):
        try:
            name = token['attributes']['name']
            address = token['attributes']['address']
            link = f"https://www.geckoterminal.com/{network}/pools/{address}"
            volume = float(token["attributes"].get("volume_usd", {}).get("h24", 0))
            liquidity = float(token["attributes"].get("reserve_in_usd", 0))
            holders = int(token["attributes"].get("pool_token_holders", 0))

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

# ✅ Commande /snip
@dp.message(Command("snip"))
async def send_tokens(message: Message):
    await message.answer("🔍 Je récupère les tokens récents...")

    sui_tokens = get_recent_tokens_sui()
    avax_tokens = get_recent_tokens_avax()
    xrp_tokens = get_recent_tokens_xrp()

    # SUI tokens
    for token in sui_tokens:
        btn = InlineKeyboardMarkup().add(
            InlineKeyboardButton("🚀 SNIPE", url=token['link'])
        )
        await message.answer(
            f"💎 Token : {token['name']} (SUI)\n🔗 [Voir sur GeckoTerminal]({token['link']})",
            parse_mode="Markdown",
            reply_markup=btn
        )

    # AVAX tokens
    for token in avax_tokens:
        btn = InlineKeyboardMarkup().add(
            InlineKeyboardButton("🚀 SNIPE", url=token['link'])
        )
        await message.answer(
            f"💎 Token : {token['name']} (AVAX)\n🔗 [Voir sur GeckoTerminal]({token['link']})",
            parse_mode="Markdown",
            reply_markup=btn
        )

    # XRP tokens ✅ NOUVEAU
    for token in xrp_tokens:
        btn = InlineKeyboardMarkup().add(
            InlineKeyboardButton("🚀 SNIPE", url=token['link'])
        )
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


