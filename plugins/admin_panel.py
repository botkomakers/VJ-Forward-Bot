import matplotlib
matplotlib.use('Agg')  # For headless environments like Render
import matplotlib.pyplot as plt
from pyrogram import Client, filters
from config import Config
from database import db
import os
import asyncio
from pyrogram.types import Message

@Client.on_message(filters.command("broadcast") & filters.user(Config.BOT_OWNER))
async def broadcast_all(client: Client, message: Message):
    if not message.reply_to_message:
        return await message.reply("❌ Reply to a message to broadcast it to all users.")

    users = await db.get_all_users()
    sent = 0
    for user_id in users:
        try:
            await message.reply_to_message.copy(chat_id=user_id)
            sent += 1
        except:
            continue
    await message.reply(f"✅ Broadcast sent to {sent} users.")

@Client.on_message(filters.command("broadcast_user") & filters.user(Config.BOT_OWNER))
async def broadcast_to_user(client: Client, message: Message):
    if len(message.command) < 3:
        return await message.reply("❌ Usage: /broadcast_user <user_id> <message>")

    try:
        user_id = int(message.command[1])
        msg = " ".join(message.command[2:])
        await client.send_message(user_id, msg)
        await message.reply(f"✅ Sent to user `{user_id}`.")
    except Exception as e:
        await message.reply(f"❌ Failed to send:\n`{e}`")

@Client.on_message(filters.command("ban") & filters.user(Config.BOT_OWNER))
async def ban_user(client: Client, message: Message):
    if len(message.command) < 2:
        return await message.reply("❌ Usage: /ban <user_id>")

    try:
        user_id = int(message.command[1])
        await db.ban_user(user_id)
        await message.reply(f"⛔ User `{user_id}` has been banned.")
    except Exception as e:
        await message.reply(f"❌ Failed to ban:\n`{e}`")

@Client.on_message(filters.command("unban") & filters.user(Config.BOT_OWNER))
async def unban_user(client: Client, message: Message):
    if len(message.command) < 2:
        return await message.reply("❌ Usage: /unban <user_id>")

    try:
        user_id = int(message.command[1])
        await db.unban_user(user_id)
        await message.reply(f"✅ User `{user_id}` has been unbanned.")
    except Exception as e:
        await message.reply(f"❌ Failed to unban:\n`{e}`")

@Client.on_message(filters.command("banlist") & filters.user(Config.BOT_OWNER))
async def show_banlist(client: Client, message: Message):
    banned_users = await db.get_banned()
    if not banned_users:
        return await message.reply("✅ No users are banned.")

    text = "**⛔ Banned Users:**\n\n"
    text += "\n".join([f"`{uid}`" for uid in banned_users])
    await message.reply(text)






#stats
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





#run

# bot/plugins/exec.p

from pyrogram import Client, filters
from pyrogram.types import Message
from database import db

@Client.on_message(filters.command("setforward") & filters.private)
async def set_forward(client: Client, message: Message):
    try:
        args = message.text.split()
        print("Received setforward command:", args)

        if len(args) != 3:
            return await message.reply_text(
                "**❗ব্যবহার:** `/setforward <from_chat_id> <to_chat_id>`",
                quote=True
            )

        try:
            from_chat = int(args[1])
            to_chat = int(args[2])
        except ValueError:
            return await message.reply_text(
                "**⚠️ ত্রুটি:** চ্যাট আইডি গুলো সংখ্যায় দিতে হবে!",
                quote=True
            )

        user_id = message.from_user.id

        # Add user if not exists
        if not await db.is_forwad_exit(user_id):
            await db.add_frwd(user_id)

        await db.update_forward(user_id, {
            "chat_id": from_chat,
            "toid": to_chat
        })

        return await message.reply_text(
            f"**✅ ফরোয়ার্ডিং সফলভাবে সেট করা হয়েছে!**\n\n**From Chat ID:** `{from_chat}`\n**To Chat ID:** `{to_chat}`",
            quote=True
        )

    except Exception as e:
        print("Error in setforward:", e)
        await message.reply_text(f"**⚠️ ত্রুটি:** `{str(e)}`", quote=True)

# ✅ অটো ফরোয়ার্ড লিসেনার (চ্যানেল পোস্ট হলে ফরোয়ার্ড করে)
@Client.on_message(filters.channel)
async def auto_forward_handler(client, message):
    try:
        all_forwarders = await db.get_all_frwd()  # Assuming this returns a list
        for user in all_forwarders:
            user_id = user['user_id']
            details = await db.get_forward_details(user_id)
            from_id = details.get("chat_id")
            to_id = details.get("toid")

            if message.chat.id == from_id:
                try:
                    await message.forward(to_id)
                except Exception as e:
                    print(f"❌ Forward Failed for user {user_id}: {e}")

    except Exception as e:
        print(f"⚠️ Auto Forward Error: {e}")