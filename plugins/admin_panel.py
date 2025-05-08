import asyncio
import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from config import Config
from database import db

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

@Client.on_message(filters.command("admin") & filters.user(Config.BOT_OWNER))
async def admin_panel(client: Client, message: Message):
    await generate_status_graph()

    total_users = await db.total_users_count()
    total_bots = await db.bot.count_documents({})
    total_userbots = await db.userbot.count_documents({})
    banned = len(await db.get_banned())
    forward_users = await db.forwad_count()

    caption = (
        "**🛠️ Admin Control Panel**\n\n"
        f"👤 Total Users: `{total_users}`\n"
        f"🤖 Bot Users: `{total_bots}`\n"
        f"👥 Userbots: `{total_userbots}`\n"
        f"⛔ Banned: `{banned}`\n"
        f"📬 Forwarders: `{forward_users}`\n\n"
        "Use the buttons below to perform actions:"
    )

    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("📢 Broadcast", callback_data="admin_broadcast")],
        [InlineKeyboardButton("📨 Direct Message", callback_data="admin_dm")],
        [InlineKeyboardButton("⛔ Ban User", callback_data="admin_ban")],
        [InlineKeyboardButton("✅ Unban User", callback_data="admin_unban")]
    ])

    await message.reply_photo("status_graph.png", caption=caption, reply_markup=keyboard)
    os.remove("status_graph.png")

@Client.on_callback_query(filters.user(Config.BOT_OWNER))
async def handle_admin_callback(client: Client, callback_query: CallbackQuery):
    data = callback_query.data

    if data == "admin_broadcast":
        await callback_query.message.reply("📢 Reply to this message with the text/media you want to broadcast to all users.")
    elif data == "admin_dm":
        await callback_query.message.reply("✉️ Reply to this message with `user_id: your message` format to send direct message.")
    elif data == "admin_ban":
        await callback_query.message.reply("⛔ Reply with the user ID you want to **ban**.")
    elif data == "admin_unban":
        await callback_query.message.reply("✅ Reply with the user ID you want to **unban**.")
    
    await callback_query.answer()

@Client.on_message(filters.reply & filters.user(Config.BOT_OWNER))
async def admin_actions(client: Client, message: Message):
    replied = message.reply_to_message

    if not replied or not replied.text:
        return

    if "broadcast" in replied.text.lower():
        users = await db.get_all_users()
        sent = 0
        for user_id in users:
            try:
                await client.send_message(user_id, message.text or message.caption)
                sent += 1
            except:
                continue
        await message.reply(f"✅ Broadcast sent to {sent} users.")
    
    elif "direct message" in replied.text.lower():
        try:
            parts = message.text.split(":", 1)
            user_id = int(parts[0].strip())
            text = parts[1].strip()
            await client.send_message(user_id, text)
            await message.reply("✅ Message sent successfully.")
        except Exception as e:
            await message.reply(f"❌ Failed to send message:\n`{e}`")
    
    elif "ban" in replied.text.lower():
        try:
            user_id = int(message.text.strip())
            await db.ban_user(user_id)
            await message.reply(f"⛔ User `{user_id}` banned successfully.")
        except Exception as e:
            await message.reply(f"❌ Failed to ban user:\n`{e}`")

    elif "unban" in replied.text.lower():
        try:
            user_id = int(message.text.strip())
            await db.unban_user(user_id)
            await message.reply(f"✅ User `{user_id}` unbanned successfully.")
        except Exception as e:
            await message.reply(f"❌ Failed to unban user:\n`{e}`")








#clear all mongobd Data



from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from config import Config
from database import db

@Client.on_message(filters.command("mongclear") & filters.user(Config.BOT_OWNER))
async def mong_clear_handler(client: Client, message: Message):
    keyboard = InlineKeyboardMarkup(
        [[
            InlineKeyboardButton("✅ Confirm Delete", callback_data="confirm_mong_clear"),
            InlineKeyboardButton("❌ Cancel", callback_data="cancel_mong_clear")
        ]]
    )
    await message.reply_text(
        "**⚠️ Are you sure you want to delete all MongoDB data?**\n\n"
        "This will wipe all collections (`users`, `bots`, `userbot`, `notify`, `channels`).\n\n"
        "Press **Confirm Delete** only if you are sure!",
        reply_markup=keyboard
    )


@Client.on_callback_query(filters.regex("^(confirm_mong_clear|cancel_mong_clear)$"))
async def confirm_clear_callback(client, callback_query):
    if callback_query.from_user.id != Config.BOT_OWNER:
        return await callback_query.answer("Access denied!", show_alert=True)

    if callback_query.data == "cancel_mong_clear":
        return await callback_query.edit_message_text("❌ MongoDB wipe canceled.")

    try:
        await db.col.drop()
        await db.bot.drop()
        await db.userbot.drop()
        await db.nfy.drop()
        await db.chl.drop()

        await callback_query.edit_message_text("✅ All MongoDB collections have been successfully deleted!")
    except Exception as e:
        await callback_query.edit_message_text(f"❌ Error while clearing MongoDB: `{e}`")