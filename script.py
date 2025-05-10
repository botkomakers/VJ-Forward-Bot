import os
from config import Config

class Script(object):

    START_TXT = """<b>Welcome {}, to the Ultimate Telegram Forward Bot!

I’m your all-in-one solution for smart, automated, and filtered forwarding between Telegram channels and groups.

Tap the <u>Help</u> button below to explore everything I can do for you.</b>"""

    HELP_TXT = """<b><u>🛠 Help & Commands</u></b>

<b>Basic Commands:</b>
• <code>/start</code> – Start the bot or check status
• <code>/forward</code> – Begin message forwarding process
• <code>/settings</code> – View and update forwarding preferences
• <code>/stop</code> – Stop ongoing forwarding session
• <code>/reset</code> – Reset all settings to default
• <code>/unequify</code> – Remove duplicated media

<b>Advanced Capabilities:</b>
• Forward from any public/private channel
• Admin-free forwarding from public chats
• Custom captions & inline buttons
• Smart duplicate message detection
• Intelligent filtering by content type
• Live status & progress tracking
• Multi-bot and userbot integration
"""

    HOW_USE_TXT = """<b><u>📌 Quick Start Guide</u></b>

<b>1. Add Bot or Userbot</b>
– Ensure the bot is added to your source and target channels
– Bot must be admin in the target channel

<b>2. Permissions Check</b>
– If the source is private:
  • Bot = admin in source OR
  • Userbot = member of source

<b>3. Set Settings</b>
– Use <code>/settings</code> to configure your filters, captions, and more

<b>4. Start Forwarding</b>
– Use <code>/forward</code> to begin
– Monitor your session with live feedback

▶️ <a href='https://youtu.be/wO1FE-lf35I'>Watch Video Tutorial</a>"""

    ABOUT_TXT = """<b>
╔═══❰ Bot Information ❱═══
║• 🤖 Bot Name: <a href="https://t.me/VJForwardBot">Forward Bot</a>
║• 👨 Creator: <a href="https://t.me/kingvj01">King VJ 👑</a>
║• 🆕 Updates: <a href="https://t.me/vj_botz">VJ Botz</a>
║• 🚀 Hosting: Ultra Fast Cloud
║• 🧠 Language: Python 3
║• 📚 Framework: Pyrogram 2.11.0
║• 🏷️ Version: 0.18.3-stable
╚═══════════════════════</b>"""

    STATUS_TXT = """
<b>
╔═══❰ Live Bot Status ❱═══
║• ⏱ Uptime: <code>{}</code>
║• 👥 Users Connected: <code>{}</code>
║• 🤖 Bots Active: <code>{}</code>
║• 🔄 Total Forwards: <code>{}</code>
╚═══════════════════════</b>
"""

    FROM_MSG = "<b>🟡 Please send the <u>last message</u> or its <u>link</u> from the source channel.</b>\n\n<code>/cancel</code> – Abort process"

    TO_MSG = "<b>🟢 Select the <u>target channel</u> below from the provided options.</b>\n\n<code>/cancel</code> – Abort process"

    SKIP_MSG = """<b>⏭ Set Number of Messages to Skip:</b>

Choose how many messages should be skipped before forwarding begins.

<b>Examples:</b>
<code>0</code> – Start from first message  
<code>5</code> – Skip first 5 messages

<code>/cancel</code> – Abort process"""

    CANCEL = "<b>❌ Operation Cancelled. You're back at the main menu.</b>"

    BOT_DETAILS = "<b><u>🤖 Bot Identity</u></b>\n<b>Name:</b> <code>{}</code>\n<b>ID:</b> <code>{}</code>\n<b>Username:</b> @{}</b>"

    USER_DETAILS = "<b><u>👤 Userbot Identity</u></b>\n<b>Name:</b> <code>{}</code>\n<b>ID:</b> <code>{}</code>\n<b>Username:</b> @{}</b>"

    TEXT = """
<b>
╔═══❰ Forwarding Summary ❱═══
║• 📩 Messages Fetched: <code>{}</code>
║• ✅ Sent: <code>{}</code>
║• 🧩 Duplicates Ignored: <code>{}</code>
║• 🗑 Deleted: <code>{}</code>
║• ⏭ Skipped: <code>{}</code>
║• 🔍 Filtered Out: <code>{}</code>
║• 📶 Current Status: <code>{}</code>
║• 📊 Progress: <code>{}</code>%
╚═══❰ {} ❱═══</b>
"""

    DUPLICATE_TEXT = """
<b>
╔═══❰ Duplicate Removal Report ❱═══
║• 📦 Files Analyzed: <code>{}</code>
║• 🗑 Removed Duplicates: <code>{}</code>
╚═══❰ {} ❱═══</b>
"""

    DOUBLE_CHECK = """<b><u>⚠️ Final Review Before Starting</u></b>

<b>Bot:</b> [{botname}](https://t.me/{botuname})  
<b>Source:</b> <code>{from_chat}</code>  
<b>Target:</b> <code>{to_chat}</code>  
<b>Skip Count:</b> <code>{skip}</code>

<b>Important:</b>
• Bot must be admin in the <u>target channel</u>  
• If source is private, userbot or bot must have access

✅ If everything looks good, hit "Yes" to begin."""

    SETTINGS_TXT = "<b>⚙️ Update your preferences below to tailor how the bot forwards your content.</b>"