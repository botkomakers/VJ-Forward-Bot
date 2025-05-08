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

main_buttons = [
    [InlineKeyboardButton('❤️ ᴏᴇᴡᴇʟᴏᴛᴇʀ ❤️', url='https://t.me/your_bot_link')],
    [InlineKeyboardButton('🔍 sᴜᴘᴘᴏʀᴛ ɢʀᴏᴜᴘ', url='https://t.me/vj_bot_disscussion'),
     InlineKeyboardButton('🤖 ᴜᴘᴅᴀᴛᴇ ᴄʜᴀɴɴᴇʟ', url='https://t.me/your_bot_link')],
    [InlineKeyboardButton('💕 Yᴏᴜᴛᴜʙᴇ', url='https://youtube.com/@your_bot_link')],
    [InlineKeyboardButton('👨‍💻 ʜᴇʟᴘ', callback_data='help'),
     InlineKeyboardButton('💁 ᴀʙᴏᴜᴛ', callback_data='about')],
    [InlineKeyboardButton('⚙ sᴇᴛᴛɪɴɢs', callback_data='settings#main')]
]

@Client.on_message(filters.private & filters.command(['start']))
async def start(client, message):
    user = message.from_user
    user_id = user.id
    first_name = user.first_name or "NoName"
    mention = user.mention
    username = f"@{user.username}" if user.username else "N/A"

    # Check and add new user
    if not await db.is_user_exist(user_id):
        await db.add_user(user_id, first_name)
        log_text = f"""
╭━━━[ 🚀 ɴᴇᴡ ᴜsᴇʀ ᴀʟᴇʀᴛ ]━━━➤
┣⪼ 🔹 ID: `{user_id}`
┣⪼ 👤 Name: {mention}
┣⪼ 🌐 Username: {username}
┣⪼ ⏰ Join Time: `{time.strftime('%Y-%m-%d %H:%M:%S')}`
╰━━━━━━━━━━━━━━━━━━━━━━➤
"""
        try:
            await client.send_message(
                chat_id=int(Config.LOG_CHANNEL),
                text=log_text,
                parse_mode="html"
            )
        except Exception as e:
            try:
                await client.send_message(
                    chat_id=int(Config.BOT_OWNER),
                    text=f"❌ Logging error: `{e}`",
                    parse_mode="html"
                )
            except:
                print(f"Logging error & notify failed: {e}")

    # Show Start Message
    reply_markup = InlineKeyboardMarkup(main_buttons)
    await client.send_photo(
        chat_id=message.chat.id,
        photo="https://i.ibb.co/Rk0dkmvm/file-1314.jpg",
        caption=Script.START_TXT.format(first_name),
        reply_markup=reply_markup
    )

@Client.on_message(filters.private & filters.command(['restart']) & filters.user(Config.BOT_OWNER))
async def restart(client, message):
    msg = await message.reply_text("<i>Trying to restarting.....</i>")
    await asyncio.sleep(5)
    await msg.edit("<i>Server restarted successfully ✅</i>")
    system("git pull -f && pip3 install --no-cache-dir -r requirements.txt")
    execle(sys.executable, sys.executable, "main.py", environ)

# HELP callback
@Client.on_callback_query(filters.regex(r'^help'))
async def helpcb(bot, query):
    buttons = [[
        InlineKeyboardButton('🤔 ʜᴏᴡ ᴛᴏ ᴜsᴇ ᴍᴇ ❓', callback_data='how_to_use')
    ],[
        InlineKeyboardButton('Aʙᴏᴜᴛ ✨️', callback_data='about'),
        InlineKeyboardButton('⚙ Sᴇᴛᴛɪɴɢs', callback_data='settings#main')
    ],[
        InlineKeyboardButton('• back', callback_data='back')
    ]]
    await query.message.edit_text(Script.HELP_TXT, reply_markup=InlineKeyboardMarkup(buttons))

# HOW TO USE callback
@Client.on_callback_query(filters.regex(r'^how_to_use'))
async def how_to_use(bot, query):
    buttons = [[InlineKeyboardButton('• back', callback_data='help')]]
    await query.message.edit_text(Script.HOW_USE_TXT, reply_markup=InlineKeyboardMarkup(buttons), disable_web_page_preview=True)

# BACK callback
@Client.on_callback_query(filters.regex(r'^back'))
async def back(bot, query):
    await query.message.edit_text(Script.START_TXT.format(query.from_user.first_name), reply_markup=InlineKeyboardMarkup(main_buttons))

# ABOUT callback
@Client.on_callback_query(filters.regex(r'^about'))
async def about(bot, query):
    buttons = [[
        InlineKeyboardButton('• back', callback_data='help'),
        InlineKeyboardButton('Stats ✨️', callback_data='status')
    ]]
    await query.message.edit_text(Script.ABOUT_TXT, reply_markup=InlineKeyboardMarkup(buttons), disable_web_page_preview=True)

# STATUS callback
@Client.on_callback_query(filters.regex(r'^status'))
async def status(bot, query):
    users_count, bots_count = await db.total_users_bots_count()
    forwardings = await db.forwad_count()
    upt = await get_bot_uptime(START_TIME)
    buttons = [[
        InlineKeyboardButton('• back', callback_data='help'),
        InlineKeyboardButton('System Stats ✨️', callback_data='systm_sts'),
    ]]
    await query.message.edit_text(
        Script.STATUS_TXT.format(upt, users_count, bots_count, forwardings),
        reply_markup=InlineKeyboardMarkup(buttons),
        disable_web_page_preview=True,
    )

# SYSTEM STATUS callback
@Client.on_callback_query(filters.regex(r'^systm_sts'))
async def sys_status(bot, query):
    ram = psutil.virtual_memory().percent
    cpu = psutil.cpu_percent()
    disk_usage = psutil.disk_usage('/')
    total_space = disk_usage.total / (1024 ** 3)
    used_space = disk_usage.used / (1024 ** 3)
    free_space = disk_usage.free / (1024 ** 3)

    text = f"""
╔════❰ sᴇʀᴠᴇʀ sᴛᴀᴛs ❱═❍⊱❁۪۪
║╭━━━━━━━━━━━━━━━➣
║┣⪼ Total Disk: <code>{total_space:.2f} GB</code>
║┣⪼ Used: <code>{used_space:.2f} GB</code>
║┣⪼ Free: <code>{free_space:.2f} GB</code>
║┣⪼ CPU: <code>{cpu}%</code>
║┣⪼ RAM: <code>{ram}%</code>
║╰━━━━━━━━━━━━━━━➣
╚══════════════════❍⊱❁۪۪
"""
    buttons = [[InlineKeyboardButton('• back', callback_data='help')]]
    await query.message.edit_text(text, reply_markup=InlineKeyboardMarkup(buttons), disable_web_page_preview=True)

# Helper to get uptime string
async def get_bot_uptime(start_time):
    uptime_seconds = int(time.time() - start_time)
    uptime_minutes = uptime_seconds // 60
    uptime_hours = uptime_minutes // 60
    uptime_days = uptime_hours // 24
    uptime_string = ""
    if uptime_days:
        uptime_string += f"{uptime_days}D "
    if uptime_hours % 24:
        uptime_string += f"{uptime_hours % 24}H "
    if uptime_minutes % 60:
        uptime_string += f"{uptime_minutes % 60}M "
    uptime_string += f"{uptime_seconds % 60}S"
    return uptime_string