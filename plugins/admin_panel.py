import matplotlib
matplotlib.use('Agg')  # Render/headless server এর জন্য
import matplotlib.pyplot as plt
from pyrogram import Client, filters
from config import Config
from database import db  # root directory থেকে database.py import
import os

async def generate_status_graph():
    total_users = await db.total_users_count()
    total_bots = await db.bot.count_documents({})
    total_userbots = await db.userbot.count_documents({})
    banned_users = len(await db.get_banned())
    forward_users = await db.forwad_count()

    labels = ['Users', 'Bot Users', 'Userbots', 'Banned', 'Forwarders']
    values = [total_users, total_bots, total_userbots, banned_users, forward_users]

    plt.figure(figsize=(10, 6))
    bars = plt.bar(labels, values, color=['#4c72b0', '#dd8452', '#55a868', '#c44e52', '#937860'])
    plt.title("📊 Bot Usage Stats", fontsize=16)
    plt.xlabel("Sections", fontsize=12)
    plt.ylabel("Count", fontsize=12)

    for bar in bars:
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2.0, yval + 0.5, int(yval), ha='center', va='bottom')

    plt.tight_layout()
    plt.savefig("status_graph.png")
    plt.close()

@Client.on_message(filters.command("status") & filters.user(Config.OWNER_ID))
async def bot_status(client, message):
    try:
        await generate_status_graph()

        total_users = await db.total_users_count()
        total_bots = await db.bot.count_documents({})
        total_userbots = await db.userbot.count_documents({})
        banned = len(await db.get_banned())
        forward_users = await db.forwad_count()

        caption = (
            "**📊 বটের বর্তমান স্ট্যাটাস:**\n\n"
            f"👤 মোট ইউজার: `{total_users}`\n"
            f"🤖 বট ইউজার: `{total_bots}`\n"
            f"👥 ইউজারবট: `{total_userbots}`\n"
            f"⛔ নিষিদ্ধ ইউজার: `{banned}`\n"
            f"📬 ফরোয়ার্ড ইউজার: `{forward_users}`\n"
        )

        await message.reply_photo("status_graph.png", caption=caption)
        os.remove("status_graph.png")

    except Exception as e:
        await message.reply_text(f"❌ গ্রাফ তৈরি করতে ব্যর্থ:\n`{e}`")