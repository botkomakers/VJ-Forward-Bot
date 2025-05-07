from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery, Message
from config import Config
from database import db
import asyncio
import time

# ✅ সকল ইউজারের জন্য /cleandup কমান্ড
@Client.on_message(filters.command("cleandup"))
async def choose_channel(client, message: Message):
    user_id = message.from_user.id
    channels = await db.get_user_channels(user_id)
    if not channels:
        return await message.reply("❌ You haven't added any channels yet.")

    btns = []
    for ch in channels:
        title = ch.get("title", "Channel")
        btns.append([InlineKeyboardButton(title, callback_data=f"udup_{ch['chat_id']}")])
    btns.append([InlineKeyboardButton("❌ Cancel", callback_data="cancel_clean")])
    await message.reply(
        "**Select a channel to scan and remove duplicate videos:**",
        reply_markup=InlineKeyboardMarkup(btns)
    )


@Client.on_callback_query(filters.regex(r"^udup_"))
async def start_dup_cleaning(client, cb: CallbackQuery):
    user_id = cb.from_user.id
    chat_id = int(cb.data.split("_")[1])
    userbot_data = await db.get_userbot(user_id)

    if not userbot_data:
        return await cb.message.edit("❌ You haven't added your userbot session yet.")

    userbot = Client(
        name=f"{user_id}",
        api_id=Config.API_ID,
        api_hash=Config.API_HASH,
        session_string=userbot_data['session']
    )

    await cb.answer("Scanning started...")
    msg = await cb.message.edit("⏳ Connecting to userbot and scanning for duplicates...")

    await userbot.start()
    seen = set()
    dup_ids = []
    total = deleted = 0
    start_time = time.time()
    last_update_time = time.time()

    try:
        async for m in userbot.get_chat_history(chat_id):
            if m.video:
                total += 1
                uid = m.video.file_unique_id
                if uid in seen:
                    dup_ids.append(m.id)
                else:
                    seen.add(uid)

            # Delete in batches of 100
            if len(dup_ids) >= 100:
                await userbot.delete_messages(chat_id, dup_ids)
                deleted += len(dup_ids)
                dup_ids.clear()

                if time.time() - last_update_time > 3:
                    await msg.edit_text(
                        f"🔄 **Scanning in progress...**\n\n"
                        f"🧾 Total processed: `{total}`\n"
                        f"🗑️ Deleted so far: `{deleted}`"
                    )
                    last_update_time = time.time()

        # Delete remaining duplicates
        if dup_ids:
            await userbot.delete_messages(chat_id, dup_ids)
            deleted += len(dup_ids)

        duration = round(time.time() - start_time, 2)

        await msg.edit_text(
            f"✅ **Cleanup Complete!**\n\n"
            f"🔍 **Messages Scanned:** `{total}`\n"
            f"🗃️ **Duplicates Deleted:** `{deleted}`\n"
            f"⏱️ **Time Taken:** `{duration} seconds`\n\n"
            f"✨ _Thank you for using the Duplicate Cleaner Bot!_"
        )

    except Exception as e:
        await msg.edit_text(f"⚠️ An error occurred:\n`{str(e)}`")
    finally:
        await userbot.stop()


@Client.on_callback_query(filters.regex("cancel_clean"))
async def cancel_cb(client, cb: CallbackQuery):
    await cb.answer("❌ Cancelled", show_alert=True)
    await cb.message.edit("❌ Duplicate cleanup has been cancelled.")