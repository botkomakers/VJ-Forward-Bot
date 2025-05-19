import asyncio, logging
from config import Config
from pyrogram import Client as VJ, idle
from typing import Union, Optional, AsyncGenerator
from logging.handlers import RotatingFileHandler
from plugins.regix import restart_forwards

# Credit: @VJ_Botz | YouTube: https://youtube.com/@Tech_VJ | Telegram: @KingVJ01

if __name__ == "__main__":
    VJBot = VJ(
        "VJ-Forward-Bot",
        bot_token=Config.BOT_TOKEN,
        api_id=Config.API_ID,
        api_hash=Config.API_HASH,
        sleep_threshold=120,
        plugins=dict(root="plugins")
    )

    async def iter_messages(
        self,
        chat_id: Union[int, str],
        limit: int,
        offset: int = 0,
    ) -> Optional[AsyncGenerator["types.Message", None]]:
        current = offset
        while True:
            new_diff = min(200, limit - current)
            if new_diff <= 0:
                return
            messages = await self.get_messages(chat_id, list(range(current, current + new_diff + 1)))
            for message in messages:
                yield message
                current += 1

    async def main():
        await VJBot.start()
        bot_info = await VJBot.get_me()
        await restart_forwards(VJBot)

        # Notify in LOG_CHANNEL after restart
        try:
            await VJBot.send_message(
                Config.LOG_CHANNEL,
                f"✅ **Bot Restarted Successfully**\n\n**Name:** {bot_info.first_name}\n**Username:** @{bot_info.username}\n**ID:** `{bot_info.id}`"
            )
        except Exception as e:
            print(f"Failed to send log message: {e}")

        print("Bot Started.")
        await idle()

    asyncio.get_event_loop().run_until_complete(main())