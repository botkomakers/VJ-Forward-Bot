import re
import base64
import asyncio
import struct
from pyrogram import Client, filters, enums
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from pyrogram.file_id import FileId
from database import db
from config import temp
from .test import get_client
from script import Script

COMPLETED_BTN = InlineKeyboardMarkup([
    [InlineKeyboardButton('💟 Support Group', url='https://t.me/VJ_Bot_Disscussion')],
    [InlineKeyboardButton('💠 Update Channel', url='https://t.me/vj_botz')]
])
CANCEL_BTN = InlineKeyboardMarkup([[InlineKeyboardButton('• Cancel', 'terminate_frwd')]])


def encode_file_id(s: bytes) -> str:
    r, n = b"", 0
    for i in s + bytes([22, 4]):
        if i == 0:
            n += 1
        else:
            if n:
                r += b"\x00" + bytes([n])
                n = 0
            r += bytes([i])
    return base64.urlsafe_b64encode(r).decode().rstrip("=")


def unpack_new_file_id(new_file_id):
    decoded = FileId.decode(new_file_id)
    return encode_file_id(
        struct.pack("<iiqq", int(decoded.file_type), decoded.dc_id, decoded.media_id, decoded.access_hash)
    )


@Client.on_message(filters.command("unequify") & filters.private)
async def unequify(client, message):
    user_id = message.from_user.id
    temp.CANCEL[user_id] = False

    if temp.lock.get(user_id) == "True":
        return await message.reply("**Please wait until the previous task is complete.**")

    _bot = await db.get_userbot(user_id)
    if not _bot:
        return await message.reply("**You need to set a userbot session using /settings first.**")

    try:
        target = await client.ask(user_id, "**Forward the last message from the target chat or paste message link.**\n/cancel - Cancel process")
    except:
        return

    if target.text and target.text.startswith("/"):
        return await message.reply("**Process cancelled!**")

    chat_id, last_msg_id = None, None

    if target.text:
        match = re.match(r"(https://)?(t\.me|telegram\.me|telegram\.dog)/(c/)?([a-zA-Z0-9_]+)/(\d+)", target.text)
        if not match:
            return await message.reply("**Invalid message link.**")
        username_or_id = match.group(4)
        last_msg_id = int(match.group(5))
        if match.group(3):  # if 'c/' is present, it's a private group/channel
            chat_id = int("-100" + username_or_id)
        else:
            chat_id = username_or_id
    elif target.forward_from_chat:
        chat_id = target.forward_from_chat.id
        last_msg_id = target.forward_from_message_id
    else:
        return await message.reply("**Invalid message. Please forward a message from the target channel/group.**")

    confirm = await client.ask(user_id, "**Send /yes to confirm or /no to cancel.**")
    if confirm.text.lower() == "/no":
        return await confirm.reply("**Process cancelled!**")

    status = await confirm.reply("⏳ Connecting to userbot and scanning for duplicates...")

    temp.lock[user_id] = "True"
    data = _bot['session']
    bot = await get_client(data)

    try:
        await bot.start()
        test = await bot.send_message(chat_id, "Testing access...")
        await test.delete()
    except Exception as e:
        temp.lock[user_id] = "False"
        return await status.edit(f"**Userbot must be admin in this chat.**\n\n`{e}`")

    MESSAGES = []
    DUPLICATES = []
    total = deleted = 0

    try:
        async for msg in bot.search_messages(chat_id=chat_id, filter=enums.MessagesFilter.DOCUMENT):
            if temp.CANCEL.get(user_id):
                temp.lock[user_id] = "False"
                return await status.edit("**Process cancelled by user.**", reply_markup=COMPLETED_BTN)

            file_id = unpack_new_file_id(msg.document.file_id)

            if file_id in MESSAGES:
                DUPLICATES.append(msg.id)
            else:
                MESSAGES.append(file_id)

            total += 1

            if len(DUPLICATES) >= 100:
                await bot.delete_messages(chat_id, DUPLICATES)
                deleted += len(DUPLICATES)
                DUPLICATES.clear()

            if total % 500 == 0:
                await status.edit(f"🔎 Scanned: `{total}` messages\n🗑️ Deleted: `{deleted}` duplicates...")

        if DUPLICATES:
            await bot.delete_messages(chat_id, DUPLICATES)
            deleted += len(DUPLICATES)

    except Exception as e:
        temp.lock[user_id] = "False"
        await bot.stop()
        return await status.edit(f"**Error occurred:** `{e}`")

    temp.lock[user_id] = "False"
    await bot.stop()
    await status.edit(
        f"✅ **Duplicate cleanup completed!**\n\n"
        f"🔍 Total Documents Scanned: `{total}`\n"
        f"🗑️ Duplicates Deleted: `{deleted}`\n\n"
        f"✨ _Thanks for using Duplicate Remover_",
        reply_markup=COMPLETED_BTN
    )