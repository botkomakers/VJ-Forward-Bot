import asyncio
import logging
from config import Config
from pyrogram import Client as VJ, idle
from plugins.regix import restart_forwards

# Don't Remove Credit Tg - @VJ_Botz
# Subscribe YouTube Channel For Amazing Bot https://youtube.com/@Tech_VJ
# Ask Doubt on telegram @KingVJ01

VJBot = VJ(
    "VJ-Forward-Bot",
    bot_token=Config.BOT_TOKEN,
    api_id=Config.API_ID,
    api_hash=Config.API_HASH,
    sleep_threshold=120,
    plugins=dict(root="plugins")
)

async def main():
    await VJBot.start()
    bot_info = await VJBot.get_me()

    # Send restart message to log channel
    await VJBot.send_message(
        chat_id=Config.LOG_CHANNEL,
        text=f"✅ **Bot Restarted Successfully**\n\n"
             f"**Bot Name:** {bot_info.first_name}\n"
             f"**Username:** @{bot_info.username or 'N/A'}\n"
             f"**ID:** `{bot_info.id}`"
    )

    await restart_forwards(VJBot)
    print("Bot Started.")
    await idle()

if __name__ == "__main__":
    asyncio.run(main())