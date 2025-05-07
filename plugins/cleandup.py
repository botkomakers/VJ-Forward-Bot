# cleandup.py
from pyrogram import Client, filters, enums
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from config import Config, temp
from database import db  # আপনি যেভাবে db বানিয়েছেন

def gen_channel_buttons(channels):
    buttons = []
    for channel in channels:
        title = channel.get("title", "Unknown")
        chat_id = channel["chat_id"]
        buttons.append([InlineKeyboardButton(title, callback_data=f"clean_{chat_id}")])
    buttons.append([InlineKeyboardButton("❌ বাতিল", callback_data="cancel_clean")])
    return InlineKeyboardMarkup(buttons)

@Client.on_message(filters.command("cleandup") & filters.user(Config.BOT_OWNER))
async def show_channel_list(client: Client, message: Message):
    user_id = message.from_user.id
    channels = await db.get_user_channels(user_id)
    if not channels:
        await message.reply("❌ আপনি কোনো চ্যানেল যোগ করেননি!")
        return
    await message.reply("🔽 নিচে যে চ্যানেলগুলো দেখছেন, সেগুলোর যেকোনো একটিতে ডুপ্লিকেট ভিডিও মুছে ফেলতে ক্লিক করুন:", reply_markup=gen_channel_buttons(channels))

@Client.on_callback_query(filters.regex(r"^clean_"))
async def clean_selected_channel(client: Client, callback_query: CallbackQuery):
    user_id = callback_query.from_user.id
    chat_id = callback_query.data.split("_")[1]
    temp.CANCEL[user_id] = False
    temp.lock[user_id] = True
    await callback_query.answer()
    msg = await callback_query.message.edit(f"🔍 ডুপ্লিকেট খোঁজা শুরু হলো\nচ্যানেল: `{chat_id}`")

    seen = set()
    duplicates = []
    total = deleted = 0

    try:
        async for m in client.search_messages(int(chat_id), filter=enums.MessagesFilter.VIDEO):
            if temp.CANCEL.get(user_id):
                await msg.edit("❌ প্রক্রিয়া বাতিল হয়েছে!")
                temp.lock[user_id] = False
                return
            if not m.video:
                continue
            total += 1
            uid = m.video.file_unique_id
            if uid in seen:
                duplicates.append(m.id)
            else:
                seen.add(uid)

            if len(duplicates) >= 100:
                await client.delete_messages(int(chat_id), duplicates)
                deleted += len(duplicates)
                duplicates = []
                await msg.edit(f"🔍 স্ক্যান: {total}\n🗑️ মুছা হয়েছে: {deleted}")

        if duplicates:
            await client.delete_messages(int(chat_id), duplicates)
            deleted += len(duplicates)

        await msg.edit(f"✅ সম্পন্ন!\nমোট স্ক্যান: {total}\nমুছা হয়েছে: {deleted}")
    except Exception as e:
        await msg.edit(f"⚠️ ত্রুটি:\n`{e}`")
    finally:
        temp.lock[user_id] = False

@Client.on_callback_query(filters.regex("cancel_clean"))
async def cancel_cleaning(client: Client, callback_query: CallbackQuery):
    await callback_query.answer("❌ বাতিল করা হলো", show_alert=True)
    await callback_query.message.edit("❌ প্রক্রিয়া বাতিল করা হয়েছে।")