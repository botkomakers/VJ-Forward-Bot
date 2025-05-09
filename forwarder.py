import logging
from telethon import TelegramClient, events
from telethon.sessions import StringSession
from config import Config
from db import db
import asyncio

# Logging setup
logging.basicConfig(level=logging.INFO)
LOGS = logging.getLogger("Forwarder")

# Constants from config
APP_ID = Config.APP_ID
API_HASH = Config.API_HASH
SESSION = Config.SESSION
BLOCKED_TEXTS = [i.strip().lower() for i in (Config.BLOCKED_TEXTS or "").split(',')]
MEDIA_FORWARD_RESPONSE = (Config.MEDIA_FORWARD_RESPONSE or "yes").lower()

FROM = [int(i) for i in (Config.FROM_CHANNEL or "").split()]
TO = [int(i) for i in (Config.TO_CHANNEL or "").split()]

# Telethon client setup
client = TelegramClient(StringSession(SESSION), APP_ID, API_HASH)

@client.on(events.NewMessage(incoming=True, chats=FROM))
async def forward_handler(event):
    try:
        message_text = event.raw_text.lower()

        if any(bad in message_text for bad in BLOCKED_TEXTS):
            LOGS.warning("Blocked message: %s", event.raw_text)
            return

        for target in TO:
            if event.media:
                if MEDIA_FORWARD_RESPONSE != 'yes':
                    return
                await client.send_message(target, event.raw_text, file=event.media)
                LOGS.info("Media forwarded to %s", target)
            else:
                await client.send_message(target, event.raw_text)
                LOGS.info("Text forwarded to %s", target)

    except Exception as e:
        LOGS.error("Error forwarding message: %s", e)

async def main():
    await client.start()
    LOGS.info("Forwarder started...")
    await client.run_until_disconnected()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        LOGS.info("Bot stopped.")