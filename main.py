import os
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.types import Message
from aiogram.filters.command import Command
from dotenv import load_dotenv
from utils import get_recent_tokens_sui, get_recent_tokens_avax, update_filters
from keep_alive import keep_alive
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

load_dotenv()

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
bot = Bot(token=TOKEN)
dp = Dispatcher()

# ✅ Commande /start
@dp.message(Command("start"))
async def send_welcome(message: Message):
    await message.answer("🚀 Sniper Bot activé. Surveillance AVAX & SUI démarrée.")

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

# ✅ Lancer le bot
async def main():
    keep_alive()
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())


