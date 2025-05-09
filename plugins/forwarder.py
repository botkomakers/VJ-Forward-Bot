from pyrogram import Client, filters
from pyrogram.types import Message
from config import Config
from database import db

user = Client(
    name="userbot_forwarder",
    api_id=Config.API_ID,
    api_hash=Config.API_HASH,
    session_string=Config.SESSION_STRING
)

@user.on_message(filters.all)
async def auto_forward(client: Client, message: Message):
    async for fwd in db.get_all_frwd():
        user_id = fwd.get('user_id')
        details = await db.get_forward_details(user_id)

        from_chat_id = details.get("chat_id")
        to_chat_id = details.get("toid")

        if message.chat.id == from_chat_id:
            try:
                await message.forward(to_chat_id)
                print(f"[{user_id}] {message.id} forwarded from {from_chat_id} to {to_chat_id}")
            except Exception as e:
                print(f"Failed to forward for user {user_id}: {e}")

user.run()