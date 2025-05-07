
import time
import asyncio
import psutil
import sys
from os import environ, execle, system

from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from config import Config
from script import Script
from database import db

START_TIME = time.time()

LOG_CHANNEL_ID = -1002589776901  # Replace with your log channel ID

# Main menu buttons
main_buttons = [[
    InlineKeyboardButton("❣️ Developer ❣️", url="https://t.me/kingvj01")
],[
    InlineKeyboardButton("🔍 Support", url="https://t.me/vj_bot_disscussion"),
    InlineKeyboardButton("🤖 Updates", url="https://t.me/vj_botz")
],[
    InlineKeyboardButton("💝 YouTube", url="https://youtube.com/@Tech_VJ")
],[
    InlineKeyboardButton("👨‍💻 Help", callback_data="help"),
    InlineKeyboardButton("💁 About", callback_data="about")
],[
    InlineKeyboardButton("⚙ Settings", callback_data="settings#main")
]]

@Client.on_message(filters.private & filters.command(['start']))
async def start(client, message):
    user = message.from_user

    # Log new user
    if not await db.is_user_exist(user.id):
        await db.add_user(user.id, user.first_name)
        try:
            mention = f"<a href='tg://user?id={user.id}'>{user.first_name}</a>"
            await client.send_message(
                chat_id=LOG_CHANNEL_ID,
                text=f"🟢 <b>New User Started the Bot</b>\n\n"
                     f"👤 Name: {mention}\n"
                     f"🆔 User ID: <code>{user.id}</code>\n"
                     f"🌐 Username: @{user.username if user.username else 'N/A'}\n"
                     f"⏰ Joined At: <code>{time.strftime('%Y-%m-%d %H:%M:%S')}</code>"
            )
        except Exception as e:
            print(f"Logging error: {e}")

    welcome_text = f"""
<b>👋 Hello {user.first_name}!</b>

<b>✨ Welcome to <a href='https://t.me/vj_botz'>VJ Renamer Bot</a>!</b>
I can help you to <b>rename files</b>, <b>change thumbnails</b>, and <b>add custom captions</b> instantly.

<b>⚡ Features:</b>
• Rename & Upload files quickly  
• Custom thumbnail support  
• Caption editor  
• High-speed servers

<b>Use the buttons below to explore more!</b>
"""

    image_url = "https://i.ibb.co/Rk0dkmvm/file-1314.jpg"

    await client.send_photo(
        chat_id=message.chat.id,
        photo=image_url,
        caption=welcome_text,
        reply_markup=InlineKeyboardMarkup(main_buttons)
    )

@Client.on_message(filters.private & filters.command(['restart']) & filters.user(Config.BOT_OWNER))
async def restart(client, message):
    msg = await message.reply_text("<i>Restarting bot...</i>")
    await asyncio.sleep(5)
    await msg.edit("<i>Bot restarted successfully ✅</i>")
    system("git pull -f && pip3 install --no-cache-dir -r requirements.txt")
    execle(sys.executable, sys.executable, "main.py", environ)

@Client.on_callback_query(filters.regex(r'^help'))
async def helpcb(bot, query):
    buttons = [[
        InlineKeyboardButton("🤔 How to use?", callback_data="how_to_use")
    ],[
        InlineKeyboardButton("About ✨", callback_data="about"),
        InlineKeyboardButton("⚙ Settings", callback_data="settings#main")
    ],[
        InlineKeyboardButton("• Back", callback_data="back")
    ]]
    await query.message.edit_text(
        text=Script.HELP_TXT,
        reply_markup=InlineKeyboardMarkup(buttons)
    )

@Client.on_callback_query(filters.regex(r'^how_to_use'))
async def how_to_use(bot, query):
    buttons = [[InlineKeyboardButton("• Back", callback_data="help")]]
    await query.message.edit_text(
        text=Script.HOW_USE_TXT,
        reply_markup=InlineKeyboardMarkup(buttons),
        disable_web_page_preview=True
    )

@Client.on_callback_query(filters.regex(r'^about'))
async def about(bot, query):
    buttons = [[
        InlineKeyboardButton("• Back", callback_data="help"),
        InlineKeyboardButton("Stats ✨", callback_data="status")
    ]]
    await query.message.edit_text(
        text=Script.ABOUT_TXT,
        reply_markup=InlineKeyboardMarkup(buttons),
        disable_web_page_preview=True
    )

@Client.on_callback_query(filters.regex(r'^status'))
async def status(bot, query):
    users_count, bots_count = await db.total_users_bots_count()
    forwardings = await db.forwad_count()
    uptime = await get_bot_uptime(START_TIME)

    buttons = [[
        InlineKeyboardButton("• Back", callback_data="help"),
        InlineKeyboardButton("System Stats ✨", callback_data="systm_sts")
    ]]

    await query.message.edit_text(
        text=Script.STATUS_TXT.format(uptime, users_count, bots_count, forwardings),
        reply_markup=InlineKeyboardMarkup(buttons),
        disable_web_page_preview=True
    )

@Client.on_callback_query(filters.regex(r'^systm_sts'))
async def sys_status(bot, query):
    ram = psutil.virtual_memory().percent
    cpu = psutil.cpu_percent()
    disk = psutil.disk_usage('/')
    total = disk.total / (1024**3)
    used = disk.used / (1024**3)
    free = disk.free / (1024**3)

    buttons = [[InlineKeyboardButton("• Back", callback_data="help")]]
    text = f"""
<b>⚙ System Stats:</b>

<b>Total Disk</b>: <code>{total:.2f} GB</code>  
<b>Used</b>: <code>{used:.2f} GB</code>  
<b>Free</b>: <code>{free:.2f} GB</code>  
<b>CPU</b>: <code>{cpu}%</code>  
<b>RAM</b>: <code>{ram}%</code>
"""

    await query.message.edit_text(
        text=text,
        reply_markup=InlineKeyboardMarkup(buttons),
        disable_web_page_preview=True
    )

async def get_bot_uptime(start_time):
    uptime_seconds = int(time.time() - start_time)
    minutes = uptime_seconds // 60
    hours = minutes // 60
    days = hours // 24

    return f"{days}d {hours % 24}h {minutes % 60}m {uptime_seconds % 60}s"