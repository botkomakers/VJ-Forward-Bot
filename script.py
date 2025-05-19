import os
from config import Config

class Script(object):

    START_TXT = """<b>𝗪𝗲𝗹𝗰𝗼𝗺𝗲 {}, 𝘁𝗼 𝘁𝗵𝗲 𝗨𝗹𝘁𝗶𝗺𝗮𝘁𝗲 𝗧𝗲𝗹𝗲𝗴𝗿𝗮𝗺 𝗙𝗼𝗿𝘄𝗮𝗿𝗱 𝗕𝗼𝘁!

𝗜’𝗺 𝗮 𝗽𝗼𝘄𝗲𝗿𝗳𝘂𝗹 𝗮𝗻𝗱 𝗮𝘂𝘁𝗼𝗺𝗮𝘁𝗲𝗱 𝘀𝗼𝗹𝘂𝘁𝗶𝗼𝗻 𝗳𝗼𝗿 𝗺𝗲𝘀𝘀𝗮𝗴𝗲 𝗳𝗼𝗿𝘄𝗮𝗿𝗱𝗶𝗻𝗴 𝗯𝗲𝘁𝘄𝗲𝗲𝗻 𝗰𝗵𝗮𝗻𝗻𝗲𝗹𝘀/𝗴𝗿𝗼𝘂𝗽𝘀.

Tap the <u>𝗛𝗲𝗹𝗽</u> button to explore all features.</b>"""

    HELP_TXT = """<b><u>🛠 𝗛𝗲𝗹𝗽 & 𝗖𝗼𝗺𝗺𝗮𝗻𝗱𝘀</u></b>

<b>𝗕𝗮𝘀𝗶𝗰 𝗖𝗼𝗺𝗺𝗮𝗻𝗱𝘀:</b>
• /start – Start the bot or check status  
• /forward – Begin message forwarding  
• /settings – Configure preferences  
• /stop – Stop current process  
• /reset – Reset to default  
• /unequify – Remove duplicates  

<b>𝗔𝗱𝘃𝗮𝗻𝗰𝗲𝗱 𝗙𝗲𝗮𝘁𝘂𝗿𝗲𝘀:</b>
• Public/Private Channel Forwarding  
• Smart Filter by Message Type  
• Custom Captions & Inline Buttons  
• Duplicate Skipping  
• Userbot Integration  
• Live Forwarding Progress  
"""

    HOW_USE_TXT = """<b><u>📌 𝗤𝘂𝗶𝗰𝗸 𝗨𝘀𝗲 𝗚𝘂𝗶𝗱𝗲</u></b>

<b>1. Add Bot or Userbot</b>  
– Add to both source and target channels  
– Make admin in target

<b>2. Permission Rules</b>  
– For private source:  
  • Bot must be admin OR  
  • Userbot must be a member  

<b>3. Configure Settings</b>  
– Use <code>/settings</code> to customize  

<b>4. Start Forwarding</b>  
– Use <code>/forward</code>  
– Monitor status live  

▶️ <a href='https://t.me/FileStore_rebot?start=Z2V0LTE5OTAxNDA3MDcxNDg0ODU'>𝗪𝗮𝘁𝗰𝗵 𝗧𝘂𝘁𝗼𝗿𝗶𝗮𝗹</a>"""

    ABOUT_TXT = """<b>
╔═══❰ 𝗕𝗼𝘁 𝗜𝗻𝗳𝗼 ❱═══
║• 🤖 Name: <a href="https://t.me/VJForwardBot">Forward Bot</a>
║• 👑 Owner: <a href="https://t.me/kingvj01">King VJ</a>
║• 🆕 Updates: <a href="https://t.me/vj_botz">VJ Botz</a>
║• ☁️ Hosting: Cloud Optimized
║• 🧠 Language: Python 3
║• 🔧 Framework: Pyrogram v2.11.0
║• 🏷️ Version: 0.18.3
╚═══════════════════════</b>"""

    STATUS_TXT = """
<b>
╔═══❰ 𝗟𝗶𝘃𝗲 𝗦𝘁𝗮𝘁𝘂𝘀 ❱═══
║• ⏱ Uptime: <code>{}</code>
║• 👥 Users: <code>{}</code>
║• 🤖 Bots: <code>{}</code>
║• 🔁 Forwards: <code>{}</code>
╚═══════════════════════</b>
"""

    FROM_MSG = "<b>📥 Send the <u>last message</u> or its <u>link</u> from the source channel.</b>\n/cancel – Abort"

    TO_MSG = "<b>📤 Choose the <u>target channel</u> below from the buttons.</b>\n/cancel – Cancel"

    SKIP_MSG = """<b>⏭ 𝗦𝗸𝗶𝗽 𝗖𝗼𝘂𝗻𝘁</b>

Enter how many messages to skip before starting.

<code>0</code> – No skip  
<code>5</code> – Skip 5 messages  

<code>/cancel</code> – Abort"""

    CANCEL = "<b>❌ 𝗣𝗿𝗼𝗰𝗲𝘀𝘀 𝗖𝗮𝗻𝗰𝗲𝗹𝗹𝗲𝗱. You're back at the main menu.</b>"

    BOT_DETAILS = "<b><u>🤖 𝗕𝗼𝘁 𝗜𝗗</u></b>\n<b>Name:</b> <code>{}</code>\n<b>ID:</b> <code>{}</code>\n<b>Username:</b> @{}</b>"

    USER_DETAILS = "<b><u>👤 𝗨𝘀𝗲𝗿𝗯𝗼𝘁 𝗜𝗗</u></b>\n<b>Name:</b> <code>{}</code>\n<b>ID:</b> <code>{}</code>\n<b>Username:</b> @{}</b>"

    TEXT = """
<b>
╔═══❰ 𝗙𝗼𝗿𝘄𝗮𝗿𝗱 𝗥𝗲𝗽𝗼𝗿𝘁 ❱═══
║• 📥 Fetched: <code>{}</code>
•
║• ✅ Sent: <code>{}</code>
•
║• 🧩 Skipped Duplicates: <code>{}</code>
•
║• 🗑 Deleted: <code>{}</code>
•
║• ⏭ Skipped: <code>{}</code>
•
║• 🔍 Filtered: <code>{}</code>
•
║• 📶 Status: <code>{}</code>
•
║• 📊 Progress: <code>{}</code>%
•
╚═══❰ {} ❱═══</b>
"""

    DUPLICATE_TEXT = """
<b>
╔═══❰ 𝗗𝘂𝗽𝗹𝗶𝗰𝗮𝘁𝗲 𝗖𝗹𝗲𝗮𝗻𝘂𝗽 ❱═══
║• 📦 Files Scanned: <code>{}</code>
║• 🗑 Removed: <code>{}</code>
╚═══❰ {} ❱═══</b>
"""

    DOUBLE_CHECK = """<b><u>⚠️ 𝗙𝗶𝗻𝗮𝗹 𝗖𝗵𝗲𝗰𝗸𝗹𝗶𝘀𝘁</u></b>

<b>Bot:</b> [{botname}](https://t.me/{botuname})  
<b>Source:</b> <code>{from_chat}</code>  
<b>Target:</b> <code>{to_chat}</code>  
<b>Skip:</b> <code>{skip}</code>

✅ Confirm the bot is:
• Admin in Target Channel  
• Has access to Source  

Hit 'Yes' if ready to proceed."""

    SETTINGS_TXT = "<b>⚙️ Customize how I forward content by using the settings below.</b>"