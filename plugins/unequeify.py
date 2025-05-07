from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message
from config import temp
from database import db
from .test import get_client
import re

COMPLETED_BTN = InlineKeyboardMarkup([
    [InlineKeyboardButton('💟 Support Group', url='https://t.me/VJ_Bot_Disscussion')],
    [InlineKeyboardButton('💠 Updates Channel', url='https://t.me/vj_botz')]
])

CANCEL_BTN = InlineKeyboardMarkup([[InlineKeyboardButton('• Cancel', 'terminate_frwd')]])

@Client.on_message(filters.command("unequify") & filters.private)
async def unequify(client, message: Message):
    user_id = message.from_user.id
    temp.CANCEL[user_id] = False
    if temp.lock.get(user_id):
        return await message.reply("Please wait for the previous task to complete.")

    # Check if userbot exists
    _bot = await db.get_userbot(user_id)
    if not _bot:
        return await message.reply("**Userbot not found. Please add it from /settings.**")

    # Ask for message link or forward
    target = await client.ask(user_id, "**Send a forwarded message or message link from the target channel/group**\n/cancel to cancel")
    if target.text and target.text.startswith("/"):
        return await message.reply("**Cancelled.**")

    chat_id, last_msg_id = None, None
    if target.text:
        match = re.match(r"(https://)?t\.me/(c/)?([\w\d_]+)/?(\d+)?", target.text.strip())
        if not match:
            return await message.reply("**Invalid message link.**")
        chat_raw = match.group(3)
        chat_id = int(f"-100{chat_raw}") if chat_raw.isdigit() else chat_raw
        last_msg_id = int(match.group(4)) if match.group(4) else None
    elif target.forward_from_chat:
        chat_id = target.forward_from_chat.id
        last_msg_id = target.forward_from_message_id
    else:
        return await message.reply("**Invalid message.**")

    confirm = await client.ask(user_id, "**Type /yes to start or /no to cancel.**")
    if confirm.text.lower() == "/no":
        return await confirm.reply("**Process cancelled.**")

    sts = await confirm.reply("⏳ Connecting and scanning...")

    try:
        # Get the userbot client and start it
        bot = await get_client(_bot['session'])
        await bot.start()
    except Exception as e:
        return await sts.edit(f"**Error connecting userbot:**\n{e}")

    try:
        await bot.send_message(chat_id, ".")
    except:
        await bot.stop()
        return await sts.edit("**Userbot has no permission in this chat. Make it admin.**")

    seen_files = set()
    duplicate_ids = []
    total, deleted = 0, 0
    temp.lock[user_id] = True

    try:
        async for msg in bot.get_chat_history(chat_id):
            if temp.CANCEL.get(user_id):
                await sts.edit("**Cancelled**", reply_markup=COMPLETED_BTN)
                await bot.stop()
                return

            if msg.document:
                total += 1
                file_uid = msg.document.file_unique_id
                if file_uid in seen_files:
                    duplicate_ids.append(msg.id)
                else:
                    seen_files.add(file_uid)

            if len(duplicate_ids) >= 50:
                await bot.delete_messages(chat_id, duplicate_ids)
                deleted += len(duplicate_ids)
                duplicate_ids.clear()

                await sts.edit(
                    f"╔════❰ ᴜɴᴇǫᴜɪғʏ sᴛᴀᴛᴜs ❱═❍⊱❁۪۪\n"
                    f"║╭━━━━━━━━━━━━━━━➣\n"
                    f"║┣⪼ ғᴇᴛᴄʜᴇᴅ ғɪʟᴇs: {total}\n"
                    f"║┣⪼ ᴅᴜᴘʟɪᴄᴀᴛᴇ ᴅᴇʟᴇᴛᴇᴅ: {deleted}\n"
                    f"║╰━━━━━━━━━━━━━━━➣\n"
                    f"╚════❰ ᴘʀᴏᴄᴇssɪɴɢ ❱══❍⊱❁۪۪",
                    reply_markup=CANCEL_BTN
                )

        if duplicate_ids:
            await bot.delete_messages(chat_id, duplicate_ids)
            deleted += len(duplicate_ids)

        await sts.edit(
            f"╔════❰ ᴜɴᴇǫᴜɪғʏ sᴛᴀᴛᴜs ❱═❍⊱❁۪۪\n"
            f"║╭━━━━━━━━━━━━━━━➣\n"
            f"║┣⪼ ғᴇᴛᴄʜᴇᴅ ғɪʟᴇs: {total}\n"
            f"║┣⪼ ᴅᴜᴘʟɪᴄᴀᴛᴇ ᴅᴇʟᴇᴛᴇᴅ: {deleted}\n"
            f"║╰━━━━━━━━━━━━━━━➣\n"
            f"╚════❰ ᴄᴏᴍᴘʟᴇᴛᴇᴅ ❱══❍⊱❁۪۪",
            reply_markup=COMPLETED_BTN
        )
    except Exception as e:
        await sts.edit(f"**Error during scan:**\n{e}")
    finally:
        temp.lock[user_id] = False
        await bot.stop()