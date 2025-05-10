"""
admin_panel.py
Telegram bot admin panel – Pyrogram (asyncio)

Features
========
✓ /admin প্যানেল বাটনগুলো
  ├─ 📢 Broadcast All        →  Reply + /broadcast   (অন্যত্র হ্যান্ডল করো)
  ├─ 📤 Broadcast to User    →  ইন্টার‍্যাকটিভ: user-id → message/forward
  ├─ ⛔ Ban / ✅ Unban        →  /ban id  /unban id
  ├─ 🚫 Show Ban List
  ├─ 📊 Bot Status           →  গ্রাফ + অটো-ডিলিট “Generating…”
  └─ 🧨 Clear MongoDB        →  দুই-ক্লিক কনফার্ম

db মডিউল-এ থাকতে হবে:
    db.bot, db.userbot, db.nfy, db.chl, db.col  ←  MongoDB collections
    db.get_banned()           → list[int]
    db.total_users_count()    → int
    db.forwad_count()         → int
    db.ban_user(id) / db.unban_user(id)

Config এ থাকতে হবে:
    BOT_OWNER  (int)    – অ্যাডমিন টেলিগ্রাম ID
"""

import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from pyrogram import Client, filters
from pyrogram.types import (
    Message,
    CallbackQuery,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)

from config import Config
from database import db   # তোমার নিজস্ব database helper

# ───────────────────────────────────────────────────────────────
# ইন-মেমরি স্টেট; রিস্টার্টে মুছে যাবে (Persistent FSM চাইলে DB ব্যাবহার করো)
admin_states: dict[int, dict] = {}      # {admin_id: {"step": str, "...": ...}}

# ───────────────────────────────────────────────────────────────
# /admin – মূল বোতাম প্যানেল
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

# ───────────────────────────────────────────────────────────────
# প্যানেল-বাটন হ্যান্ডলার
@Client.on_callback_query(filters.regex(r"^admin_"))
async def admin_buttons(client: Client, cb: CallbackQuery):
    if cb.from_user.id != Config.BOT_OWNER:
        return await cb.answer("Access Denied!", show_alert=True)

    action = cb.data.split("_", 1)[1]
    await cb.answer()      # remove loading animation

    # --- simple help prompts ----------
    if action == "broadcast_all":
        return await cb.message.reply(
            "ℹ️ Reply to any message with `/broadcast` to send it to **all users**."
        )
    if action == "ban_user":
        return await cb.message.reply("📝 Use command:\n`/ban <user_id>`")
    if action == "unban_user":
        return await cb.message.reply("📝 Use command:\n`/unban <user_id>`")

    # --- interactive broadcast to single user ----------
    if action == "broadcast_user":
        admin_states[cb.from_user.id] = {"step": "awaiting_user_id"}
        return await cb.message.reply("🔢 **Enter the Telegram user-ID** you want to message:")

    # --- show ban list ----------
    if action == "banlist":
        banned = await db.get_banned()
        text = "✅ No users are banned." if not banned else \
               "**⛔ Banned Users:**\n" + "\n".join(f"`{uid}`" for uid in banned)
        return await cb.message.reply(text)

    # --- status ----------
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
        plt.savefig("stats.png"); plt.close()

        caption = (
            "**📊 Bot Stats:**\n\n"
            f"👤 Total Users: `{total_users}`\n"
            f"🤖 Bot Users: `{total_bots}`\n"
            f"👥 Userbots:   `{total_userbot}`\n"
            f"⛔ Banned:      `{banned}`\n"
            f"📬 Forwarders: `{forwarders}`"
        )
        await client.send_photo(cb.message.chat.id, "stats.png", caption=caption)
        await wait.delete();  os.remove("stats.png")
        return

    # --- mongodb clear confirm ----------
    if action == "mongclear":
        kb = InlineKeyboardMarkup([[
            InlineKeyboardButton("✅ Confirm Delete", callback_data="confirm_mongclear"),
            InlineKeyboardButton("❌ Cancel",         callback_data="cancel_mongclear"),
        ]])
        return await cb.message.reply(
            "**⚠️ Confirm MongoDB Deletion**\nThis will erase all bot data!",
            reply_markup=kb,
        )

# ───────────────────────────────────────────────────────────────
# MongoDB wipe confirmation
@Client.on_callback_query(filters.regex(r"^(confirm_mongclear|cancel_mongclear)$"))
async def confirm_wipe(_: Client, cb: CallbackQuery):
    if cb.from_user.id != Config.BOT_OWNER:
        return await cb.answer("Access denied!", show_alert=True)

    if cb.data == "cancel_mongclear":
        return await cb.edit_message_text("❌ MongoDB wipe canceled.")

    try:
        await db.col.drop();      await db.bot.drop()
        await db.userbot.drop();  await db.nfy.drop(); await db.chl.drop()
        await db.banned.drop()
        await cb.edit_message_text("✅ All MongoDB collections deleted successfully!")
    except Exception as e:
        await cb.edit_message_text(f"❌ Error during MongoDB clear:\n`{e}`")

# ───────────────────────────────────────────────────────────────
# ইন্টার‍্যাকটিভ Broadcast-to-User FSM
@Client.on_message(filters.private & filters.user(Config.BOT_OWNER))
async def broadcast_to_user_fsm(client: Client, msg: Message):
    aid = msg.from_user.id
    if aid not in admin_states:
        return   # no pending interaction

    state = admin_states[aid]["step"]

    # STEP 1 – waiting for user-ID
    if state == "awaiting_user_id":
        try:
            target = int(msg.text.strip())
            admin_states[aid] = {"step": "awaiting_message", "target_id": target}
            return await msg.reply(
                "📩 Great! Now **send any message or forward** one – "
                "I'll deliver it to that user."
            )
        except ValueError:
            return await msg.reply("❌ Please send a valid numeric Telegram user-ID.")

    # STEP 2 – waiting for the message to forward
    if state == "awaiting_message":
        target = admin_states[aid]["target_id"]
        try:
            if msg.forward_from or msg.forward_from_chat:
                await msg.forward(target)
            else:
                await client.copy_message(target, msg.chat.id, msg.id)

            await msg.reply(f"✅ Message successfully sent to `{target}`.")
        except Exception as e:
            await msg.reply(f"❌ Failed to send message:\n`{e}`")
        finally:
            admin_states.pop(aid, None)   # reset FSM

# ───────────────────────────────────────────────────────────────
# /ban  /unban  commands
@Client.on_message(filters.command("ban") & filters.user(Config.BOT_OWNER))
async def ban_cmd(_: Client, msg: Message):
    if len(msg.command) != 2:
        return await msg.reply("❌ Usage: `/ban <user_id>`")
    try:
        uid = int(msg.command[1])
        await db.ban_user(uid)
        await msg.reply(f"⛔ User `{uid}` banned.")
    except Exception as e:
        await msg.reply(f"❌ Error:\n`{e}`")

@Client.on_message(filters.command("unban") & filters.user(Config.BOT_OWNER))
async def unban_cmd(_: Client, msg: Message):
    if len(msg.command) != 2:
        return await msg.reply("❌ Usage: `/unban <user_id>`")
    try:
        uid = int(msg.command[1])
        await db.unban_user(uid)
        await msg.reply(f"✅ User `{uid}` unbanned.")
    except Exception as e:
        await msg.reply(f"❌ Error:\n`{e}`")









from pyrogram import Client, filters
from pyrogram.types import Message
from config import Config
import aiohttp

bot = Client(
    "SongFinderBot",
    bot_token=Config.BOT_TOKEN,
    api_id=Config.API_ID,
    api_hash=Config.API_HASH
)

# JioSaavn Song Search
async def get_song(query):
    api = f"https://saavn.dev/api/search/songs?query={query}"
    async with aiohttp.ClientSession() as session:
        async with session.get(api) as resp:
            data = await resp.json()
            if not data.get("data"):
                return None
            first = data["data"]["results"][0]
            return {
                "title": first["name"],
                "artist": ", ".join([a["name"] for a in first["primaryArtists"]]),
                "media_url": first["downloadUrl"][-1]["link"],
                "image": first["image"][2]["link"]
            }

@bot.on_message(filters.command("song"))
async def start(client, message: Message):
    await message.reply("Send me a song name and I'll find the audio for you!")

@bot.on_message(filters.text & ~filters.command("song"))
async def song_search(client, message: Message):
    query = message.text
    msg = await message.reply("🔍 Searching for your song...")

    try:
        song = await get_song(query)
        if not song:
            return await msg.edit("❌ No song found!")

        await client.send_audio(
            chat_id=message.chat.id,
            audio=song["media_url"],
            title=song["title"],
            performer=song["artist"],
            thumb=song["image"]
        )
        await msg.delete()
    except Exception as e:
        await msg.edit(f"❌ Failed to fetch song:\n`{e}`")

bot.run()