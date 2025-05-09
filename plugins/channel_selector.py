from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from database import db

bot = Client("channel_selector_bot")

user_channels_cache = {}

@bot.on_message(filters.command("setforward"))
async def select_from_channel(client, message: Message):
    user_id = message.from_user.id
    channels = await db.get_user_channels(user_id)
    
    if not channels:
        return await message.reply("❌ আপনি কোনো চ্যানেল যোগ করেননি।")

    buttons = [
        [InlineKeyboardButton(text=ch['title'], callback_data=f"fromch_{ch['chat_id']}")]
        for ch in channels
    ]
    user_channels_cache[user_id] = {"channels": channels}
    await message.reply("🔰 কোন চ্যানেল থেকে ফরওয়ার্ড হবে?", reply_markup=InlineKeyboardMarkup(buttons))


@bot.on_callback_query(filters.regex(r"^fromch_"))
async def select_to_channel(client: Client, query: CallbackQuery):
    user_id = query.from_user.id
    from_chat_id = int(query.data.split("_")[1])

    user_channels_cache[user_id]['from'] = from_chat_id
    channels = user_channels_cache[user_id]['channels']
    buttons = [
        [InlineKeyboardButton(text=ch['title'], callback_data=f"toch_{ch['chat_id']}")]
        for ch in channels if ch['chat_id'] != from_chat_id
    ]

    await query.message.edit("🎯 কোন চ্যানেলে ফরওয়ার্ড হবে?", reply_markup=InlineKeyboardMarkup(buttons))


@bot.on_callback_query(filters.regex(r"^toch_"))
async def finalize_forward(client: Client, query: CallbackQuery):
    user_id = query.from_user.id
    to_chat_id = int(query.data.split("_")[1])
    from_chat_id = user_channels_cache[user_id].get('from')

    if not from_chat_id:
        return await query.answer("❌ Source চ্যানেল পাওয়া যায়নি", show_alert=True)

    # Save forward data in DB
    await db.add_frwd(user_id)
    await db.update_forward(user_id, {
        'chat_id': from_chat_id,
        'toid': to_chat_id
    })

    await query.message.edit(f"✅ অটো ফরওয়ার্ড সেটআপ সম্পন্ন!\n\n**From:** `{from_chat_id}`\n**To:** `{to_chat_id}`")