from telethon import TelegramClient, events
from config import API_ID, API_HASH, SOURCE_CHANNEL, TARGET_CHANNEL
from database import Db  # তুমি যেভাবে ইউজারবট সেশন আনো

print("Fetching userbot session from database...")

# ডেটাবেস থেকে সেশন রিড
session_string = Db().get_userbot()  # এই ফাংশন তোমার কোডে আছে ধরে নিচ্ছি

if not session_string:
    print("❌ ইউজারবট সেশন পাওয়া যায়নি! দয়া করে সেট করুন।")
    exit()

# Telethon client শুরু
client = TelegramClient("userbot", API_ID, API_HASH).start(session=session_string)

@client.on(events.NewMessage(chats=SOURCE_CHANNEL))
async def auto_forward(event):
    try:
        await client.forward_messages(
            entity=TARGET_CHANNEL,
            messages=event.message
        )
        print(f"✅ ফরওয়ার্ড হয়েছে: {event.message.id}")
    except Exception as e:
        print(f"⚠️ ফরওয়ার্ডে সমস্যা: {e}")

print("✅ অটো ফরওয়ার্ড বট চালু হয়েছে...")
client.run_until_disconnected()