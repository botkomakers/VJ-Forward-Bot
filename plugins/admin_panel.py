import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from pyrogram import Client, filters
from pyrogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton

from config import Config
from database import db

admin_states: dict[int, dict] = {}  # FSM state

@Client.on_message(filters.command("admin") & filters.user(Config.BOT_OWNER))
async def admin_panel(_: Client, msg: Message):
    buttons = [
        [InlineKeyboardButton("📢 Broadcast All",   callback_data="admin_broadcast_all")],
        [InlineKeyboardButton("📤 Broadcast to User", callback_data="admin_broadcast_user")],
        [
            InlineKeyboardButton("⛔ Ban User",  callback_data="admin_ban_user"),
            InlineKeyboardButton("✅ Unban User", callback_data="admin_unban_user"),
        ],
        [InlineKeyboardButton("🚫 Show Ban List", callback_data="admin_banlist")],
        [InlineKeyboardButton("📊 Bot Status",    callback_data="admin_status")],
        [InlineKeyboardButton("🧨 Clear MongoDB", callback_data="admin_mongclear")],
    ]
    await msg.reply(
        "**🛠 Welcome to the Admin Panel!**",
        reply_markup=InlineKeyboardMarkup(buttons),
    )

@Client.on_callback_query(filters.regex(r"^admin_"))
async def admin_buttons(client: Client, cb: CallbackQuery):
    if cb.from_user.id != Config.BOT_OWNER:
        return await cb.answer("Access Denied!", show_alert=True)

    action = cb.data.split("_", 1)[1]
    await cb.answer()

    if action == "broadcast_all":
        return await cb.message.reply("ℹ️ Reply to any message with `/broadcast` to send it to **all users**.")
    if action == "ban_user":
        return await cb.message.reply("📝 Use command:\n`/ban <user_id>`")
    if action == "unban_user":
        return await cb.message.reply("📝 Use command:\n`/unban <user_id>`")
    if action == "broadcast_user":
        admin_states[cb.from_user.id] = {"step": "awaiting_user_id"}
        return await cb.message.reply("🔢 **Enter the Telegram user-ID** you want to message:")

    if action == "banlist":
        banned = await db.get_banned()
        text = "✅ No users are banned." if not banned else \
               "**⛔ Banned Users:**\n" + "\n".join(f"`{uid}`" for uid in banned)
        return await cb.message.reply(text)

    if action == "status":
        wait = await cb.message.reply("⚙️ Generating status...")

        total_users   = await db.total_users_count()
        total_bots    = await db.bot.count_documents({})
        total_userbot = await db.userbot.count_documents({})
        banned        = len(await db.get_banned())
        forwarders    = await db.forwad_count()

        labels = ["Users", "Bot Users", "Userbots", "Banned", "Forwarders"]
        values = [total_users, total_bots, total_userbot, banned, forwarders]

        plt.figure(figsize=(9, 5))
        bars = plt.bar(labels, values)
        for bar in bars:
            plt.text(bar.get_x() + bar.get_width()/2, bar.get_height()+.5,
                     f"{int(bar.get_height())}", ha="center")
        plt.title("Bot Usage Statistics")
        plt.tight_layout()