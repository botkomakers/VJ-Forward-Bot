import os
import sys
import asyncio
import time
import psutil
from os import environ, execle, system

from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from database import db
from config import Config
from script import Script

START_TIME = time.time()

# ── Modern, Clean UI Buttons ────────────────────────────────
main_buttons = [
    [InlineKeyboardButton("🆘 Help", callback_data="help"),
     InlineKeyboardButton("ℹ️ About", callback_data="about")],
    [InlineKeyboardButton("⚙️ Settings", callback_data="settings#main")],
    [InlineKeyboardButton("💬 Join Support Group", url="https://t.me/vj_bot_disscussion")],
    [InlineKeyboardButton("👨‍💻 Developer", url="https://t.me/movie_channel8"),
     InlineKeyboardButton("📢 Updates", url="https://t.me/movie_channel8")],
    [InlineKeyboardButton("▶️ Subscribe on YouTube", url="https://youtube.com/@movie_channel8")]
]

# ── /start Handler ─────────────────────────────────────────────
@Client.on_message(filters.private & filters.command(['start']))
async def start(client, message):
    user = message.from_user
    is_new_user = not await db.is_user_exist(user.id)

    if is_new_user:
        await db.add_user(user.id, user.first_name, user.username)

        # প্রোফাইল পিক নেওয়ার চেষ্টা
        try:
            photos = await client.get_profile_photos(user.id, limit=1)
            if photos:
                photo = photos[0].file_id
            else:
                photo = Config.DEFAULT_IMAGE
        except:
            photo = Config.DEFAULT_IMAGE

        caption = (
            f"**New User Joined**\n\n"
            f"**Name:** `{user.first_name}`\n"
            f"**Username:** @{user.username if user.username else 'N/A'}\n"
            f"**User ID:** `{user.id}`\n"
            f"**Link:** [Profile](tg://user?id={user.id})"
        )

        # লক চ্যানেলে ইউজার নোটিফিকেশন পাঠানো
        try:
            await client.send_photo(
                chat_id=Config.LOCK_CHANNEL_ID,
                photo=photo,
                caption=caption
            )
        except Exception as e:
            print(f"Failed to notify lock channel: {e}")

    # ইউজারকে ওয়েলকাম রেসপন্স
    reply_markup = InlineKeyboardMarkup(main_buttons)
    await message.reply_photo(
        photo="https://i.ibb.co/DHZqgKxX/photo-2025-05-19-03-02-03-7505986774653468688.jpg",
        caption=Script.START_TXT.format(user.first_name),
        reply_markup=reply_markup
    )

# ── Restart Command ────────────────────────────────────────────
@Client.on_message(filters.private & filters.command(['restart']) & filters.user(Config.BOT_OWNER))
async def restart(client, message):
    msg = await message.reply_text("<i>Restarting server...</i>")
    await asyncio.sleep(5)
    await msg.edit("<i>Server restarted successfully ✅</i>")
    system("git pull -f && pip3 install --no-cache-dir -r requirements.txt")
    execle(sys.executable, sys.executable, "main.py", environ)

# ── Restart Command ────────────────────────────────────────────
@Client.on_message(filters.private & filters.command(['restart']) & filters.user(Config.BOT_OWNER))
async def restart(client, message):
    msg = await message.reply_text("<i>Restarting server...</i>")
    await asyncio.sleep(5)
    await msg.edit("<i>Server restarted successfully ✅</i>")
    system("git pull -f && pip3 install --no-cache-dir -r requirements.txt")
    execle(sys.executable, sys.executable, "main.py", environ)

# ── Help Menu ──────────────────────────────────────────────────
@Client.on_callback_query(filters.regex(r'^help'))
async def helpcb(bot, query):
    buttons = [
        [InlineKeyboardButton("❓ How to Use", callback_data="how_to_use")],
        [
            InlineKeyboardButton("ℹ️ About", callback_data="about"),
            InlineKeyboardButton("⚙️ Settings", callback_data="settings#main")
        ],
        [InlineKeyboardButton("⬅️ Back to Home", callback_data="back")]
    ]
    await query.message.edit_text(
        text=Script.HELP_TXT,
        reply_markup=InlineKeyboardMarkup(buttons)
    )

@Client.on_callback_query(filters.regex(r'^how_to_use'))
async def how_to_use(bot, query):
    buttons = [[InlineKeyboardButton("⬅️ Back to Help", callback_data="help")]]
    await query.message.edit_text(
        text=Script.HOW_USE_TXT,
        reply_markup=InlineKeyboardMarkup(buttons),
        disable_web_page_preview=True
    )

@Client.on_callback_query(filters.regex(r'^back'))
async def back(bot, query):
    await query.message.edit_text(
        text=Script.START_TXT.format(query.from_user.first_name),
        reply_markup=InlineKeyboardMarkup(main_buttons)
    )

# ── About Menu ─────────────────────────────────────────────────
@Client.on_callback_query(filters.regex(r'^about'))
async def about(bot, query):
    buttons = [
        [
            InlineKeyboardButton("⬅️ Back", callback_data="help"),
            InlineKeyboardButton("📊 View Stats", callback_data="status")
        ]
    ]
    await query.message.edit_text(
        text=Script.ABOUT_TXT,
        reply_markup=InlineKeyboardMarkup(buttons),
        disable_web_page_preview=True
    )

# ── Status Menu ────────────────────────────────────────────────
@Client.on_callback_query(filters.regex(r'^status'))
async def status(bot, query):
    users_count, bots_count = await db.total_users_bots_count()
    forwardings = await db.forwad_count()
    uptime = await get_bot_uptime(START_TIME)
    buttons = [
        [
            InlineKeyboardButton("⬅️ Back", callback_data="help"),
            InlineKeyboardButton("🖥 System Info", callback_data="systm_sts")
        ]
    ]
    await query.message.edit_text(
        text=Script.STATUS_TXT.format(uptime, users_count, bots_count, forwardings),
        reply_markup=InlineKeyboardMarkup(buttons),
        disable_web_page_preview=True
    )

# ── System Stats ───────────────────────────────────────────────
@Client.on_callback_query(filters.regex(r'^systm_sts'))
async def sys_status(bot, query):
    buttons = [[InlineKeyboardButton("⬅️ Back", callback_data="help")]]
    ram = psutil.virtual_memory().percent
    cpu = psutil.cpu_percent()
    disk = psutil.disk_usage('/')
    total = disk.total / (1024**3)
    used = disk.used / (1024**3)
    free = disk.free / (1024**3)

    text = f"""
<b>🖥 Server Status</b>
━━━━━━━━━━━━━━━━━━━
• Total Disk: <code>{total:.2f} GB</code>
• Used Disk: <code>{used:.2f} GB</code>
• Free Disk: <code>{free:.2f} GB</code>
• CPU Usage: <code>{cpu}%</code>
• RAM Usage: <code>{ram}%</code>
━━━━━━━━━━━━━━━━━━━
"""
    await query.message.edit_text(
        text,
        reply_markup=InlineKeyboardMarkup(buttons),
        disable_web_page_preview=True
    )

# ── Uptime Utility ─────────────────────────────────────────────
async def get_bot_uptime(start_time):
    uptime_seconds = int(time.time() - start_time)
    minutes = uptime_seconds // 60
    hours = minutes // 60
    days = hours // 24
    return f"{days}d {hours % 24}h {minutes % 60}m {uptime_seconds % 60}s"