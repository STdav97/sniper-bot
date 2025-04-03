import os
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.types import Message
from aiogram.filters.command import Command
from dotenv import load_dotenv
from utils import get_recent_tokens_sui, get_recent_tokens_avax
from keep_alive import keep_alive
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

load_dotenv()

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
bot = Bot(token=TOKEN)
dp = Dispatcher()

# Message /start
@dp.message(Command("start"))
async def send_welcome(message: Message):
    await message.answer("🚀 Sniper Bot activé. Surveillance AVAX & SUI démarrée.")

# Commande /snip
@dp.message(Command("snip"))
async def send_tokens(message: Message):
    await message.answer("⏳ Je récupère les tokens récents...")

    sui_tokens = get_recent_tokens_sui()
    avax_tokens = get_recent_tokens_avax()

    response = "🟢 **Tokens récents**\n\n"
    response += "🚀 **SUI :**\n"
    for token in sui_tokens:
        response += f"- {token['name']} : [{token['link']}]({token['link']})\n"

    response += "\n🔺 **AVAX :**\n"
    for token in avax_tokens:
        response += f"- {token['name']} : [{token['link']}]({token['link']})\n"

    await message.answer(response, parse_mode="Markdown")

async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
async def main():
    keep_alive()
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
