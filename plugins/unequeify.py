from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery, Message
from config import Config
from database import db
import asyncio
import time

# ✅ /cleandup কমান্ড
@Client.on_message(filters.command("cleandup"))
async def choose_channel(client, message: Message):
    user_id = message.from_user.id
    channels = await db.get_user_channels(user_id)

    btns = []
    if channels:
        for ch in channels:
            title = ch.get("title", "Channel")
            btns.append([InlineKeyboardButton(title, callback_data=f"udup_{ch['chat_id']}")])
    btns.append([InlineKeyboardButton("➕ অন্য চ্যানেল", callback_data="udup_custom")])
    btns.append([InlineKeyboardButton("❌ বাতিল করুন", callback_data="cancel_clean")])
    await message.reply(
        "✅ যে চ্যানেল থেকে ডুপ্লিকেট ভিডিও মুছতে চান, তা নির্বাচন করুন বা অন্য চ্যানেল দিন:",
        reply_markup=InlineKeyboardMarkup(btns)
    )

# ✅ অন্য চ্যানেলের অনুরোধ
@Client.on_callback_query(filters.regex("udup_custom"))
async def ask_channel_info(client, cb: CallbackQuery):
    await cb.answer()
    await cb.message.edit(
        "🔁 দয়া করে চ্যানেল থেকে একটি মেসেজ ফরওয়ার্ড করুন **অথবা** চ্যানেলের @username / chat ID দিন।\n\n"
        "যেমন:\n`@yourchannel` বা `-1001234567890`"
    )
    await db.set_user_state(cb.from_user.id, "awaiting_custom_channel")

# ✅ ইউজারের চ্যানেল ইনপুট হ্যান্ডলিং
@Client.on_message(filters.text & filters.private)
async def handle_channel_input(client, message: Message):
    user_id = message.from_user.id
    state = await db.get_user_state(user_id)

    if state != "awaiting_custom_channel":
        return

    await db.set_user_state(user_id, None)  # reset state
    chat_id = None

    if message.forward_from_chat:
        chat_id = message.forward_from_chat.id
    else:
        try:
            chat_id = int(message.text.strip()) if message.text.strip().startswith("-100") else message.text.strip()
        except:
            return await message.reply("❌ সঠিক চ্যানেল ID বা ইউজারনেম দিন।")

    dummy_cb = type("Dummy", (object,), {
        "from_user": message.from_user,
        "message": message,
        "data": f"udup_{chat_id}",
        "answer": lambda *a, **kw: None
    })()

    await start_dup_cleaning(client, dummy_cb)

# ✅ ডুপ্লিকেট ক্লিনার ফাংশন
@Client.on_callback_query(filters.regex(r"^udup_"))
async def start_dup_cleaning(client, cb: CallbackQuery):
    user_id = cb.from_user.id
    chat_id = cb.data.split("_", 1)[1]
    try:
        chat_id = int(chat_id) if chat_id.startswith("-") else chat_id
    except:
        return await cb.message.edit("❌ ভুল চ্যানেল ID/username।")

    userbot_data = await db.get_userbot(user_id)
    if not userbot_data:
        return await cb.message.edit("❌ আপনি এখনো ইউজারবট সেশন যোগ করেননি।")

    userbot = Client(
        name=f"{user_id}",
        api_id=Config.API_ID,
        api_hash=Config.API_HASH,
        session_string=userbot_data['session']
    )

    await cb.message.edit(f"🔍 `{chat_id}` চ্যানেলে ডুপ্লিকেট ভিডিও স্ক্যান করা হচ্ছে...")

    await userbot.start()
    seen = set()
    dup_ids = []
    total = deleted = 0
    start_time = time.time()

    try:
        async for msg in userbot.get_chat_history(chat_id):
            if msg.video:
                total += 1
                uid = msg.video.file_unique_id
                if uid in seen:
                    dup_ids.append(msg.id)
                else:
                    seen.add(uid)

            if len(dup_ids) >= 100:
                await userbot.delete_messages(chat_id, dup_ids)
                deleted += len(dup_ids)
                dup_ids.clear()

                await cb.message.edit(
                    f"🔄 স্ক্যান চলছে...\n"
                    f"প্রসেস হয়েছে: `{total}`\n"
                    f"ডিলিট হয়েছে: `{deleted}` ডুপ্লিকেট"
                )

        if dup_ids:
            await userbot.delete_messages(chat_id, dup_ids)
            deleted += len(dup_ids)

        duration = time.time() - start_time
        await cb.message.edit(
            f"✅ **ডুপ্লিকেট ক্লিন শেষ!**\n\n"
            f"মোট স্ক্যান: `{total}`\n"
            f"ডিলিট হয়েছে: `{deleted}`\n"
            f"সময় লেগেছে: `{round(duration, 2)}s`"
        )
    except Exception as e:
        await cb.message.edit(f"⚠️ ত্রুটি:\n`{e}`")
    finally:
        await userbot.stop()

# ❌ বাতিল
@Client.on_callback_query(filters.regex("cancel_clean"))
async def cancel_cb(client, cb: CallbackQuery):
    await cb.answer("❌ বাতিল করা হয়েছে", show_alert=True)
    await cb.message.edit("ডুপ্লিকেট ক্লিন বাতিল করা হয়েছে।")