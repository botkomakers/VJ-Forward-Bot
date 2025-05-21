import os
import time
import requests
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO

from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from database import db
from config import Config
from script import Script

START_TIME = time.time()

LOG_CHANNEL = Config.LOG_CHANNEL
TEMPLATE_PATH = "template.jpg"  # Upload your image as template.jpg
DEFAULT_IMG = "https://i.ibb.co/DHZqgKxX/photo-2025-05-19-03-02-03-7505986774653468688.jpg"

main_buttons = [
    [InlineKeyboardButton("🆘 Help", callback_data="help"),
     InlineKeyboardButton("ℹ️ About", callback_data="about")],
    [InlineKeyboardButton("⚙️ Settings", callback_data="settings#main")],
    [InlineKeyboardButton("💬 Join Support Group", url="https://t.me/moviesearch6g")],
    [InlineKeyboardButton("👨‍💻 Developer", url="https://t.me/movie_channel8"),
     InlineKeyboardButton("📢 Updates", url="https://t.me/movie_channel8")],
    [InlineKeyboardButton("▶️ Subscribe on YouTube", url="https://youtube.com/@movie_channel8")]
]

@Client.on_message(filters.private & filters.command(['start']))
async def start(client, message):
    user = message.from_user
    if not await db.is_user_exist(user.id):
        await db.add_user(user.id, user.first_name)

        # fetch profile picture or use default
        try:
            photos = await client.get_profile_photos(user.id, limit=1)
            if photos.total_count > 0:
                file = await client.download_media(photos[0].file_id)
            else:
                file = requests.get(DEFAULT_IMG).content
        except:
            file = requests.get(DEFAULT_IMG).content

        # Load template
        bg = Image.open(TEMPLATE_PATH).convert("RGBA")
        draw = ImageDraw.Draw(bg)

        # Paste profile picture
        try:
            pfp = Image.open(file if isinstance(file, str) else BytesIO(file)).resize((250, 250)).convert("RGBA")
            mask = Image.new("L", (250, 250), 0)
            draw_mask = ImageDraw.Draw(mask)
            draw_mask.ellipse((0, 0, 250, 250), fill=255)
            bg.paste(pfp, (930, 200), mask)
        except Exception as e:
            print(f"Profile paste error: {e}")

        # Add text (use custom font if needed)
        font = ImageFont.truetype("arial.ttf", 40)
        draw.text((100, 220), f"NAME : {user.first_name}", fill="white", font=font)
        draw.text((100, 290), f"USERNAME : @{user.username if user.username else 'N/A'}", fill="white", font=font)
        draw.text((100, 360), f"USER ID : {user.id}", fill="white", font=font)

        # Save final image
        final = BytesIO()
        final.name = "welcome.jpg"
        bg = bg.convert("RGB")  # <-- এই লাইন যুক্ত করো
        bg.save(final, "JPEG")
        final.seek(0)

        await client.send_photo(
            chat_id=LOG_CHANNEL,
            photo=final,
            caption=f"**New User Joined!**\n\n**ID:** `{user.id}`\n**Name:** {user.mention}\n**Username:** @{user.username if user.username else 'N/A'}"
        )

    # Send main welcome message
    reply_markup = InlineKeyboardMarkup(main_buttons)
    await client.send_photo(
        chat_id=message.chat.id,
        photo=DEFAULT_IMG,
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