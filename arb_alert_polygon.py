from aiogram import Bot
import os

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")  # Mets ton chat_id ici (int)

bot = Bot(token=TOKEN)

async def send_arb_alert(msg):
    await bot.send_message(CHAT_ID, msg)
import asyncio

# ... dans ta boucle principale
if opportunity_detected:
    message = "🚨 ARBITRAGE DETECTÉ SUR POLYGON !"
    asyncio.run(send_arb_alert(message))
