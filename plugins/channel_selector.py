from pyrogram import Client, filters
from pyrogram.types import Message
from database import db

@Client.on_message(filters.command("setforward") & filters.private)
async def set_forward(client, message: Message):
    args = message.text.split()
    if len(args) != 3:
        return await message.reply("Usage:\n`/setforward <source_channel_id> <target_channel_id>`", quote=True)

    source_id = int(args[1])
    target_id = int(args[2])
    user_id = message.from_user.id

    details = await db.get_forward_details(user_id)
    details.update({
        "chat_id": source_id,
        "toid": target_id
    })

    await db.update_forward(user_id, details)
    await db.add_frwd(user_id)
    await message.reply(f"✅ Forwarding Enabled:\nFrom: `{source_id}`\nTo: `{target_id}`")







from pyrogram import Client, filters
from database import db

@Client.on_message(filters.channel)
async def auto_forward(client, message):
    try:
        source_chat = message.chat.id
        async for user in db.get_all_frwd():
            details = user.get("details", {})
            if details.get("chat_id") == source_chat:
                to_channel = details.get("toid")
                if to_channel:
                    await message.forward(to_channel)
    except Exception as e:
        print(f"[!] Auto Forward Error: {e}")