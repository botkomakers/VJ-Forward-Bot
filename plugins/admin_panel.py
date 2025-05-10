from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from config import Config
from database import db
import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

# Admin Panel UI
@Client.on_message(filters.command("admin") & filters.user(Config.BOT_OWNER))
async def admin_panel(client, message: Message):
    buttons = [
        [InlineKeyboardButton("📢 Broadcast All", callback_data="admin_broadcast_all")],
        [InlineKeyboardButton("📤 Broadcast to User", callback_data="admin_broadcast_user")],
        [InlineKeyboardButton("⛔ Ban User", callback_data="admin_ban_user"),
         InlineKeyboardButton("✅ Unban User", callback_data="admin_unban_user")],
        [InlineKeyboardButton("🚫 Show Ban List", callback_data="admin_banlist")],
        [InlineKeyboardButton("📊 Bot Status", callback_data="admin_status")],
        [InlineKeyboardButton("🧨 Clear MongoDB", callback_data="admin_mongclear")]
    ]
    await message.reply("**🛠 Welcome to the Admin Panel!**", reply_markup=InlineKeyboardMarkup(buttons))


# Admin Button Handler
@Client.on_callback_query(filters.regex("^admin_"))
async def handle_admin_panel(client, callback):
    if callback.from_user.id != Config.BOT_OWNER:
        return await callback.answer("Access Denied!", show_alert=True)

    action = callback.data.split("_", 1)[1]
    await callback.answer()

    if action == "broadcast_all":
        await callback.message.reply("ℹ️ Reply to any message and type `/broadcast` to send it to all users.")

    elif action == "broadcast_user":
        await callback.message.reply("📝 Use command:\n`/broadcast_user <user_id> <message>`")

    elif action == "ban_user":
        await callback.message.reply("📝 Use command:\n`/ban <user_id>`")

    elif action == "unban_user":
        await callback.message.reply("📝 Use command:\n`/unban <user_id>`")

    elif action == "banlist":
        banned_users = await db.get_banned()
        if not banned_users:
            return await callback.message.reply("✅ No users are banned.")
        text = "**⛔ Banned Users:**\n" + "\n".join([f"`{uid}`" for uid in banned_users])
        await callback.message.reply(text)

    elif action == "status":
        msg = await callback.message.reply("⚙️ Generating status...")

        total_users = await db.total_users_count()
        total_bots = await db.bot.count_documents({})
        total_userbots = await db.userbot.count_documents({})
        banned = len(await db.get_banned())
        forward_users = await db.forwad_count()

        labels = ['Users', 'Bot Users', 'Userbots', 'Banned', 'Forwarders']
        values = [total_users, total_bots, total_userbots, banned, forward_users]

        plt.figure(figsize=(10, 6))
        bars = plt.bar(labels, values, color=['#4c72b0', '#dd8452', '#55a868', '#c44e52', '#937860'])
        for bar in bars:
            yval = bar.get_height()
            plt.text(bar.get_x() + bar.get_width()/2.0, yval + 0.5, int(yval), ha='center')
        plt.title("Bot Usage Statistics")
        plt.tight_layout()
        plt.savefig("status_graph.png")
        plt.close()

        caption = (
            "**📊 Bot Stats:**\n\n"
            f"👤 Total Users: `{total_users}`\n"
            f"🤖 Bot Users: `{total_bots}`\n"
            f"👥 Userbots: `{total_userbots}`\n"
            f"⛔ Banned: `{banned}`\n"
            f"📬 Forwarders: `{forward_users}`"
        )
        await client.send_photo(callback.message.chat.id, "status_graph.png", caption=caption)
        await msg.delete()
        os.remove("status_graph.png")

    elif action == "mongclear":
        keyboard = InlineKeyboardMarkup([[
            InlineKeyboardButton("✅ Confirm Delete", callback_data="confirm_mongclear"),
            InlineKeyboardButton("❌ Cancel", callback_data="cancel_mongclear")
        ]])
        await callback.message.reply(
            "**⚠️ Confirm MongoDB Deletion**\nThis will erase all bot data!",
            reply_markup=keyboard
        )


# MongoDB Clear Confirmation
@Client.on_callback_query(filters.regex("^(confirm_mongclear|cancel_mongclear)$"))
async def confirm_clear_callback(client, callback_query):
    if callback_query.from_user.id != Config.BOT_OWNER:
        return await callback_query.answer("Access denied!", show_alert=True)

    if callback_query.data == "cancel_mongclear":
        return await callback_query.edit_message_text("❌ MongoDB wipe canceled.")

    try:
        await db.col.drop()
        await db.bot.drop()
        await db.userbot.drop()
        await db.nfy.drop()
        await db.chl.drop()
        await callback_query.edit_message_text("✅ All MongoDB collections deleted successfully!")
    except Exception as e:
        await callback_query.edit_message_text(f"❌ Error during MongoDB clear:\n`{e}`")