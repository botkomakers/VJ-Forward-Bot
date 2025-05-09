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










import asyncio
import pytz
from datetime import datetime
from config import LOG_CHANNEL, BOT_TOKEN, API_ID, API_HASH

async def send_restart_log(app):
    tz = pytz.timezone("Asia/Kolkata")
    now = datetime.now(tz)
    date_str = now.strftime("%d %B, %Y")
    time_str = now.strftime("%I:%M:%S %p")

    version = "v2.0.106"
    layer = "158"

    text = f"""**✅ Video Renamer Bot Is Restarted !!**

📅 **Date :** {date_str}
⏰ **Time :** {time_str}
🌐 **Timezone :** Asia/Kolkata

🉐 **Version :** `{version}` (Layer {layer})
"""
    try:
        await app.send_message(LOG_CHANNEL, text)
        print("✅ Restart log sent to log channel.")
    except Exception as e:
        print(f"❌ Failed to send restart log: {e}")




if __name__ == "__main__":
    app = Client("bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)
    app.start()
    asyncio.get_event_loop().run_until_complete(send_restart_log(app))
    app.run()
