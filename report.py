# report.py
from aiogram import Router, types
from aiogram.filters.command import Command
import json
import os

router = Router()

@router.message(Command("report"))
async def report_handler(message: types.Message):
    try:
        if not os.path.exists("snipes_log.json"):
            await message.answer("❌ Aucun snipe enregistré pour le moment.")
            return

        with open("snipes_log.json", "r") as f:
            lines = f.readlines()

        if not lines:
            await message.answer("📭 Aucun snipe à afficher pour l'instant.")
            return

        snipes = [json.loads(line) for line in lines]
        # Tri par gain décroissant
        snipes = sorted(snipes, key=lambda x: x["gain_percent"], reverse=True)

        # Limite à 5 meilleurs snipes
        top_snipes = snipes[:5]
        response = "📊 *Top Snipes Testnet*\n\n"

        for s in top_snipes:
            response += (
                f"🔹 *{s['token']}* ({s['network']})\n"
                f"📈 Gain : +{s['gain_percent']}%\n"
                f"🕓 {s['sniped_at'][:19].replace('T', ' ')} UTC\n"
                f"🔗 TX : `{s['tx_hash']}`\n\n"
            )

        await message.answer(response, parse_mode="Markdown")

    except Exception as e:
        await message.answer(f"❌ Erreur lors du rapport : {e}")
