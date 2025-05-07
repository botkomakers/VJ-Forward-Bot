from pyrogram import Client, filters
from pyrogram.types import Message, CallbackQuery
from config import Config
from database import db
import time

@Client.on_message(filters.command("cleandup") & filters.private)
async def cleandup_start(client, message: Message):
    user_id = message.from_user.id
    await message.reply(
        "🔁 দয়া করে **তোমার চ্যানেল থেকে একটি পোস্ট ফরোয়ার্ড করো**\n"
        "অথবা চ্যানেলের @username / chat ID পাঠাও যেখান থেকে ডুপ্লিকেট ভিডিও মুছতে চাও।"
    )
    await db.set_user_state(user_id, "awaiting_channel_input")

@Client.on_message(filters.private & filters.text)
async def handle_text_or_forward(client, message: Message):
    user_id = message.from_user.id
    state = await db.get_user_state(user_id)
    if state != "awaiting_channel_input":
        return

    await db.set_user_state(user_id, None)  # reset state
    chat_id = None

    # ফরওয়ার্ড করা চ্যানেল থেকে ID
    if message.forward_from_chat:
        chat_id = message.forward_from_chat.id
    else:
        # @username বা -1001234567890
        try:
            text = message.text.strip()
            chat_id = int(text) if text.startswith("-100") else text
        except:
            return await message.reply("❌ সঠিক চ্যানেল ইউজারনেম বা আইডি দিন।")

    # ডুপ্লিকেট ক্লিনার কল করো
    await clean_duplicates(client, message, user_id, chat_id)

async def clean_duplicates(client, message: Message, user_id: int, chat_id):
    userbot_data = await db.get_userbot(user_id)
    if not userbot_data:
        return await message.reply("❌ আপনি এখনো ইউজারবট সেশন যোগ করেননি।")

    await message.reply(f"🔍 `{chat_id}` চ্যানেলে ডুপ্লিকেট ভিডিও খোঁজা হচ্ছে...")

    userbot = Client(
        name=str(user_id),
        api_id=Config.API_ID,
        api_hash=Config.API_HASH,
        session_string=userbot_data['session']
    )

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

                await message.reply(
                    f"🔄 স্ক্যান চলছে...\n"
                    f"স্ক্যান: `{total}`\n"
                    f"ডিলিট: `{deleted}`"
                )

        if dup_ids:
            await userbot.delete_messages(chat_id, dup_ids)
            deleted += len(dup_ids)

        duration = round(time.time() - start_time, 2)
        await message.reply(
            f"✅ **ডুপ্লিকেট ক্লিন শেষ!**\n\n"
            f"মোট স্ক্যান: `{total}`\n"
            f"ডিলিট হয়েছে: `{deleted}` ভিডিও\n"
            f"সময় লেগেছে: `{duration} সেকেন্ড`"
        )
    except Exception as e:
        await message.reply(f"⚠️ ত্রুটি:\n`{e}`")
    finally:
        await userbot.stop()