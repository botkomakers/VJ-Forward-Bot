import matplotlib
matplotlib.use('Agg')  # For headless environments like Render
import matplotlib.pyplot as plt
from pyrogram import Client, filters
from config import Config
from database import db
import os
import asyncio

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
    plt.title("📊 Bot Usage Statistics", fontsize=16)
    plt.xlabel("Categories", fontsize=12)
    plt.ylabel("Count", fontsize=12)

    for bar in bars:
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2.0, yval + 0.5, int(yval), ha='center', va='bottom')

    plt.tight_layout()
    plt.savefig("status_graph.png")
    plt.close()

@Client.on_message(filters.command("status") & filters.user(Config.BOT_OWNER))
async def bot_status(client, message):
    loading_msg = await message.reply("⚙️ Collecting stats and generating graph...")

    try:
        await generate_status_graph()

        total_users = await db.total_users_count()
        total_bots = await db.bot.count_documents({})
        total_userbots = await db.userbot.count_documents({})
        banned = len(await db.get_banned())
        forward_users = await db.forwad_count()

        caption = (
            "**📊 Current Bot Status:**\n\n"
            f"👤 Total Users: `{total_users}`\n"
            f"🤖 Bot Users: `{total_bots}`\n"
            f"👥 Userbots: `{total_userbots}`\n"
            f"⛔ Banned Users: `{banned}`\n"
            f"📬 Forward Users: `{forward_users}`\n"
        )

        await message.reply_photo("status_graph.png", caption=caption)
        await loading_msg.delete()
        os.remove("status_graph.png")

    except Exception as e:
        await loading_msg.edit(f"❌ Failed to generate graph:\n`{e}`")