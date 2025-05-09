# Don't Remove Credit Tg - @VJ_Botz
# Subscribe YouTube Channel For Amazing Bot https://youtube.com/@Tech_VJ
# Ask Doubt on telegram @KingVJ01

import asyncio, logging
from config import Config
from pyrogram import Client as VJ, idle
from typing import Union, Optional, AsyncGenerator
from logging.handlers import RotatingFileHandler
from plugins.regix import restart_forwards

# Don't Remove Credit Tg - @VJ_Botz
# Subscribe YouTube Channel For Amazing Bot https://youtube.com/@Tech_VJ
#Ask Doubt on telegram @KingVJ01

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
        """Iterate through a chat sequentially.
        This convenience method does the same as repeatedly calling :meth:`~pyrogram.Client.get_messages` in a loop, thus saving
        you from the hassle of setting up boilerplate code. It is useful for getting the whole chat messages with a
        single call.
        Parameters:
            chat_id (``int`` | ``str``):
                Unique identifier (int) or username (str) of the target chat.
                For your personal cloud (Saved Messages) you can simply use "me" or "self".
                For a contact that exists in your Telegram address book you can use his phone number (str).
                
            limit (``int``):
                Identifier of the last message to be returned.
                
            offset (``int``, *optional*):
                Identifier of the first message to be returned.
                Defaults to 0.
        Returns:
            ``Generator``: A generator yielding :obj:`~pyrogram.types.Message` objects.
        Example:
            .. code-block:: python
                for message in app.iter_messages("pyrogram", 1, 15000):
                    print(message.text)
        """
        current = offset
        while True:
            new_diff = min(200, limit - current)
            if new_diff <= 0:
                return
            messages = await self.get_messages(chat_id, list(range(current, current+new_diff+1)))
            for message in messages:
                yield message
                current += 1
               
    async def main():
        await VJBot.start()
        bot_info  = await VJBot.get_me()
        await restart_forwards(VJBot)
        print("Bot Started.")
        await idle()

    asyncio.get_event_loop().run_until_complete(main())



# Don't Remove Credit Tg - @VJ_Botz
# Subscribe YouTube Channel For Amazing Bot https://youtube.com/@Tech_VJ
# Ask Doubt on telegram @KingVJ01










import os
from datetime import datetime
from pytz import timezone
from pyrogram import Client, __version__
from pyrogram.raw.all import layer
from config import Config
from aiohttp import web
from route import web_server
import pyrogram.utils
import pyromod
from pyrogram import filters
from pyrogram.types import Message

# -----------------------------
# Logging All Private Messages
# -----------------------------
@Client.on_message(filters.private & ~filters.command(["start", "help", "status", "broadcast", "ban", "unban"]))
async def log_all_private_messages(bot, message: Message):
    try:
        user = message.from_user
        text = message.text or "No Text"
        await bot.send_message(
            chat_id=Config.LOG_CHANNEL,
            text=f"**#NEW_MESSAGE_LOGGED**\n\n**From:** `{user.id}` - {user.first_name}\n**Username:** @{user.username if user.username else 'N/A'}\n\n**Message:**\n{text}"
        )
    except Exception as e:
        print(f"[LOGGING ERROR] => {e}")

# -----------------------------
# Pyrogram Minimum ID Fix
# -----------------------------
pyrogram.utils.MIN_CHAT_ID = -999999999999
pyrogram.utils.MIN_CHANNEL_ID = -1009999999999

# -----------------------------
# Bot Class
# -----------------------------
class Bot(Client):
    def __init__(self):
        super().__init__(
            name="vj-forward-bot",
            api_id=Config.API_ID,
            api_hash=Config.API_HASH,
            bot_token=Config.BOT_TOKEN,
            workers=200,
            plugins={"root": "plugins"},
            sleep_threshold=15,
        )

    async def start(self):
        await super().start()
        me = await self.get_me()
        self.mention = me.mention
        self.username = me.username
        self.uptime = Config.BOT_UPTIME

        if Config.WEBHOOK:
            app_runner = web.AppRunner(await web_server())
            await app_runner.setup()
            PORT = int(os.environ.get("PORT", 8000))
            await web.TCPSite(app_runner, "0.0.0.0", PORT).start()

        print(f"{me.first_name} Is Started.....✨️")

        for id in Config.BOT_OWNER:
            try:
                await self.send_message(id, f"**{me.first_name} Is Started...**")
            except Exception as e:
                print(f"Error sending message to admin {id}: {e}")

        if Config.LOG_CHANNEL:
            try:
                curr = datetime.now(timezone("Asia/Kolkata"))
                date = curr.strftime('%d %B, %Y')
                time = curr.strftime('%I:%M:%S %p')
                await self.send_message(
                    Config.LOG_CHANNEL,
                    f"**{me.mention} Is Restarted !!**\n\n📅 Date : `{date}`\n⏰ Time : `{time}`\n🌐 Timezone : `Asia/Kolkata`\n\n🉐 Version : `v{__version__} (Layer {layer})`"
                )
            except Exception as e:
                print(f"Error sending message to LOG_CHANNEL: {e}")

    async def stop(self, *args):
        await super().stop()
        print(f"{self.mention} is stopped.")


# -----------------------------
# Create App Instance
# -----------------------------
app = Bot()

# -----------------------------
# Run the Bot
# -----------------------------
if __name__ == "__main__":
    app.run()