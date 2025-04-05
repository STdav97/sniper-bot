# commands_simulation.py

from aiogram import Router, types
from aiogram.filters.command import Command
import subprocess

router = Router()

# 🔹 /simulate_avax
@router.message(Command("simulate_avax"))
async def simulate_avax_handler(message: types.Message):
    await message.answer("🚀 Lancement de la simulation AVAX testnet...")
    try:
        output = subprocess.check_output(["python", "sniper_avax_testnet.py"], text=True)
        await message.answer(f"✅ AVAX terminé\n```{output[-1500:]}```", parse_mode="Markdown")
    except Exception as e:
        await message.answer(f"❌ Erreur AVAX : {e}")

# 🔹 /simulate_sui
@router.message(Command("simulate_sui"))
async def simulate_sui_handler(message: types.Message):
    await message.answer("🌐 Lancement de la simulation SUI testnet...")
    try:
        output = subprocess.check_output(["python", "sniper_sui_testnet.py"], text=True)
        await message.answer(f"✅ SUI terminé\n```{output[-1500:]}```", parse_mode="Markdown")
    except Exception as e:
        await message.answer(f"❌ Erreur SUI : {e}")

# 🔹 /simulate_all
@router.message(Command("simulate_all"))
async def simulate_all_handler(message: types.Message):
    await message.answer("⚡ Lancement des simulations AVAX + SUI...")
    try:
        avax_output = subprocess.check_output(["python", "sniper_avax_testnet.py"], text=True)
        sui_output = subprocess.check_output(["python", "sniper_sui_testnet.py"], text=True)

        result_msg = (
            "✅ *Simulation terminée !*\n\n"
            "📡 *AVAX Testnet :*\n"
            f"```{avax_output[-800:]}```\n\n"
            "🌐 *SUI Testnet :*\n"
            f"```{sui_output[-800:]}```"
        )

        await message.answer(result_msg, parse_mode="Markdown")

    except Exception as e:
        await message.answer(f"❌ Erreur lors de la simulation : {e}")
