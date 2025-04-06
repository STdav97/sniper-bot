from aiogram import Router, types
from aiogram.filters.command import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from sniper_avax_testnet_v2 import run_avax_simulation
from sniper_sui_testnet import run_sui_simulation
import json

router = Router()

# 🔹 /simulate_avax
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
                    f"💎 Token : {token['name']} (AVAX)
"
                    f"📊 Gain simulé : x{token['gain']}
"
                    f"🔗 [Voir sur GeckoTerminal]({token['link']})"
                )
                btn = InlineKeyboardMarkup(inline_keyboard=[
                    [InlineKeyboardButton(text="🚀 BUY NOW", url=token["link"])]
                ])
                await message.answer(text, parse_mode="Markdown", reply_markup=btn)
    except Exception as e:
        await message.answer(f"❌ Erreur lecture fichier : {e}")

# 🔹 /simulate_sui
@router.message(Command("simulate_sui"))
async def simulate_sui_handler(message: types.Message):
    await message.answer("🌐 Lancement de la simulation SUI testnet...")
    run_sui_simulation()

    try:
        with open("snipes_log.json", "r") as f:
            data = json.load(f)
            sui_tokens = [t for t in data if t["network"] == "SUI"][-5:]

            for token in sui_tokens:
                text = (
                    f"💎 Token : {token['name']} (SUI)
"
                    f"📊 Gain simulé : x{token['gain']}
"
                    f"🔗 [Voir sur GeckoTerminal]({token['link']})"
                )
                btn = InlineKeyboardMarkup(inline_keyboard=[
                    [InlineKeyboardButton(text="🚀 BUY NOW", url=token["link"])]
                ])
                await message.answer(text, parse_mode="Markdown", reply_markup=btn)
    except Exception as e:
        await message.answer(f"❌ Erreur lecture fichier : {e}")

# 🔹 /simulate_all
@router.message(Command("simulate_all"))
async def simulate_all_handler(message: types.Message):
    await message.answer("⚡ Lancement des simulations AVAX + SUI...")
    run_avax_simulation()
    run_sui_simulation()

    try:
        with open("snipes_log.json", "r") as f:
            data = json.load(f)
            avax_tokens = [t for t in data if t["network"] == "AVAX"][-3:]
            sui_tokens = [t for t in data if t["network"] == "SUI"][-3:]

            for token in avax_tokens + sui_tokens:
                text = (
                    f"💎 Token : {token['name']} ({token['network']})
"
                    f"📊 Gain simulé : x{token['gain']}
"
                    f"🔗 [Voir sur GeckoTerminal]({token['link']})"
                )
                btn = InlineKeyboardMarkup(inline_keyboard=[
                    [InlineKeyboardButton(text="🚀 BUY NOW", url=token["link"])]
                ])
                await message.answer(text, parse_mode="Markdown", reply_markup=btn)
    except Exception as e:
        await message.answer(f"❌ Erreur lecture fichier : {e}")

