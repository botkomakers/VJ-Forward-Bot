from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery, Message
from config import Config, temp
from database import db
import asyncio

@Client.on_message(filters.command("cleandup"))
async def choose_channel(client, message: Message):
    user_id = message.from_user.id
    channels = await db.get_user_channels(user_id)
    if not channels:
        return await message.reply("❌ কোনো চ্যানেল যোগ করা হয়নি।")

    btns = []
    for ch in channels:
        title = ch.get("title", "Channel")
        btns.append([InlineKeyboardButton(title, callback_data=f"udup_{ch['chat_id']}")])
    btns.append([InlineKeyboardButton("❌ বাতিল", callback_data="cancel_clean")])
    await message.reply("নিচের চ্যানেল থেকে বেছে নিন ডুপ্লিকেট মুছতে:", reply_markup=InlineKeyboardMarkup(btns))


@Client.on_callback_query(filters.regex(r"^udup_"))
async def start_dup_cleaning(client, cb: CallbackQuery):
    user_id = cb.from_user.id
    chat_id = int(cb.data.split("_")[1])
    userbot_data = await db.get_userbot(user_id)

    if not userbot_data:
        return await cb.message.edit("❌ আপনি এখনও userbot যুক্ত করেননি!")

    userbot = Client(
        name=f"{user_id}",
        api_id=Config.API_ID,
        api_hash=Config.API_HASH,
        session_string=userbot_data['session']
    )

    await cb.answer("স্ক্যান শুরু হচ্ছে...")
    await cb.message.edit(f"🔎 `{chat_id}` চ্যানেলে স্ক্যান চলছে...")

    await userbot.start()
    seen = set()
    dup_ids = []
    total = deleted = 0

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
                await cb.message.edit(f"🔄 স্ক্যানিং: {total} বার্তা\n🗑️ ডিলিটেড: {deleted}")

        if dup_ids:
            await userbot.delete_messages(chat_id, dup_ids)
            deleted += len(dup_ids)

        await cb.message.edit(f"✅ কাজ শেষ!\nমোট স্ক্যান: {total}\nডিলিটেড: {deleted}")
    except Exception as e:
        await cb.message.edit(f"⚠️ ত্রুটি:\n`{e}`")
    finally:
        await userbot.stop()

@Client.on_callback_query(filters.regex("cancel_clean"))
async def cancel_cb(client, cb: CallbackQuery):
    await cb.answer("❌ বাতিল করা হয়েছে", show_alert=True)
    await cb.message.edit("ডুপ্লিকেট মুছা বাতিল করা হয়েছে।")