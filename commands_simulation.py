from aiogram import Router, types
from aiogram.filters.command import Command
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
import json
from sniper_avax_testnet_v2 import run_avax_simulation

router = Router()

@router.message(Command("simulate_avax"))
async def simulate_avax_handler(message: types.Message):
    await message.answer("🚀 Lancement de la simulation AVAX testnet...")
    run_avax_simulation()

    try:
        with open("snipes_log.json", "r") as f:
            data = json.load(f)
            avax_tokens = [t for t in data if t["network"] == "AVAX"][-5:]

            for token in avax_tokens:
                text = (
                    f"💎 Token : {token['name']} (AVAX)\n"
                    f"📊 Gain simulé : +{token['gain']}%\n"
                    f"🔗 [Voir sur DexScreener]({token['link']})"
                )
                btn = InlineKeyboardMarkup(inline_keyboard=[
                    [InlineKeyboardButton(text="🚀 BUY NOW (DexScreener)", url=token["link"])]
                ])
                await message.answer(text, parse_mode="Markdown", reply_markup=btn)

    except Exception as e:
        await message.answer(f"❌ Erreur lecture fichier : {e}")

   

