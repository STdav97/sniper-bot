import os
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.types import Message
from aiogram.filters.command import Command
from dotenv import load_dotenv
from utils import get_recent_tokens_sui, get_recent_tokens_avax
from keep_alive import keep_alive
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

load_dotenv()

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def send_welcome(message: Message):
    await message.answer("🚀 Sniper Bot activé. Surveillance AVAX & SUI démarrée.")

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

async def main():
    keep_alive()
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())

