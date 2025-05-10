# bot/plugins/admin_panel.py

import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from config import Config
from database import db

OWNER_FILTER = filters.user(Config.BOT_OWNER)

# Main Admin Panel Button
@Client.on_message(filters.command("admin") & OWNER_FILTER)
async def show_admin_panel(client, message: Message):
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("📣 Broadcast All", callback_data="broadcast_all")],
        [InlineKeyboardButton("🔨 Ban/Unban User", callback_data="ban_unban")],
        [InlineKeyboardButton("📊 Status", callback_data="status")],
        [InlineKeyboardButton("🗑 Clear DB", callback_data="clear_db")]
    ])
    await message.reply("⚙️ **Admin Control Panel**", reply_markup=keyboard)

# Broadcast All
@Client.on_callback_query(filters.regex("^broadcast_all$") & OWNER_FILTER)
async def broadcast_prompt(client, query: CallbackQuery):
    await query.message.edit("✏️ Reply to a message with `/broadcast` to send it to all users.")

@Client.on_message(filters.command("broadcast") & OWNER_FILTER)
async def broadcast_all(client, message: Message):
    if not message.reply_to_message:
        return await message.reply("❌ Reply to a message to broadcast.")
    sent = 0
    async for user in db.get_all_users():
        try:
            await message.reply_to_message.copy(chat_id=user["id"])
            sent += 1
        except: continue
    await message.reply(f"✅ Broadcast sent to `{sent}` users.")

# Ban/Unban
@Client.on_callback_query(filters.regex("^ban_unban$") & OWNER_FILTER)
async def ban_menu(client, query: CallbackQuery):
    await query.message.edit("Use:\n- `/ban <user_id>`\n- `/unban <user_id>`\n- `/banlist`")

@Client.on_message(filters.command("ban") & OWNER_FILTER)
async def ban_user(client, message: Message):
    if len(message.command) < 2:
        return await message.reply("Usage: /ban <user_id>")
    try:
        user_id = int(message.command[1])
        await db.ban_user(user_id)
        await message.reply(f"⛔ User `{user_id}` banned.")
    except Exception as e:
        await message.reply(f"❌ Error:\n`{e}`")

@Client.on_message(filters.command("unban") & OWNER_FILTER)
async def unban_user(client, message: Message):
    if len(message.command) < 2:
        return await message.reply("Usage: /unban <user_id>")
    try:
        user_id = int(message.command[1])
        await db.remove_ban(user_id)
        await message.reply(f"✅ User `{user_id}` unbanned.")
    except Exception as e:
        await message.reply(f"❌ Error:\n`{e}`")

@Client.on_message(filters.command("banlist") & OWNER_FILTER)
async def show_banlist(client, message: Message):
    banned = await db.get_banned()
    if not banned:
        return await message.reply("✅ No users are banned.")
    text = "**⛔ Banned Users:**\n" + "\n".join([f"`{uid}`" for uid in banned])
    await message.reply(text)

# Status Generator
async def generate_status_graph():
    total_users = await db.total_users_count()
    total_bots = await db.bot.count_documents({})
    total_userbots = await db.userbot.count_documents({})
    banned = len(await db.get_banned())
    forward_users = await db.forwad_count()

    labels = ['Users', 'Bots', 'Userbots', 'Banned', 'Forwarders']
    values = [total_users, total_bots, total_userbots, banned, forward_users]
    plt.figure(figsize=(10, 6))
    bars = plt.bar(labels, values, color=['#4c72b0', '#dd8452', '#55a868', '#c44e52', '#937860'])
    plt.title("Bot Statistics")
    for bar in bars:
        plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5, f'{int(bar.get_height())}', ha='center')
    plt.tight_layout()
    plt.savefig("status.png")
    plt.close()

@Client.on_callback_query(filters.regex("^status$") & OWNER_FILTER)
async def bot_status(client, query: CallbackQuery):
    loading = await query.message.edit("⚙️ Generating status...")
    try:
        await generate_status_graph()
        total_users = await db.total_users_count()
        total_bots = await db.bot.count_documents({})
        total_userbots = await db.userbot.count_documents({})
        banned = len(await db.get_banned())
        forward_users = await db.forwad_count()
        caption = (
            "**📊 Bot Status:**\n\n"
            f"👤 Users: `{total_users}`\n"
            f"🤖 Bots: `{total_bots}`\n"
            f"👥 Userbots: `{total_userbots}`\n"
            f"⛔ Banned: `{banned}`\n"
            f"📬 Forwarders: `{forward_users}`"
        )
        await query.message.reply_photo("status.png", caption=caption)
        await loading.delete()
        os.remove("status.png")
    except Exception as e:
        await query.message.edit(f"❌ Error: `{e}`")

# Clear MongoDB
@Client.on_callback_query(filters.regex("^clear_db$") & OWNER_FILTER)
async def confirm_clear(client, query: CallbackQuery):
    keyboard = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("✅ Confirm", callback_data="confirm_mong_clear"),
            InlineKeyboardButton("❌ Cancel", callback_data="cancel_mong_clear")
        ]
    ])
    await query.message.edit("⚠️ Confirm to delete all MongoDB data!", reply_markup=keyboard)

@Client.on_callback_query(filters.regex("^(confirm_mong_clear|cancel_mong_clear)$") & OWNER_FILTER)
async def handle_clear(client, query: CallbackQuery):
    if query.data == "cancel_mong_clear":
        return await query.message.edit("❌ Cancelled.")
    try:
        await db.col.drop()
        await db.bot.drop()
        await db.userbot.drop()
        await db.nfy.drop()
        await db.chl.drop()
        await query.message.edit("✅ MongoDB cleared successfully.")
    except Exception as e:
        await query.message.edit(f"❌ Error: `{e}`")