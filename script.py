import os
from config import Config

class Script(object):

    START_TXT = """<b>Hi {},

I am an advanced forward bot.
I can automatically forward messages from one channel to another with smart filtering and customization.

Tap the <u>Help</u> button below to learn more about how I work!</b>"""

    HELP_TXT = """<b><u>🔹 Help Guide</u></b>

<b>Available Commands:</b>
⏺️ <code>/start</code> - Check if the bot is alive  
⏺️ <code>/forward</code> - Start forwarding messages  
⏺️ <code>/settings</code> - Customize your bot settings  
⏺️ <code>/cleandup</code> - Remove duplicate media files  
⏺️ <code>/stop</code> - Stop active forwarding tasks  
⏺️ <code>/reset</code> - Reset all your configurations  

<b>Features:</b>
✅ Forward from public channels without admin rights  
✅ Custom captions & inline buttons  
✅ Smart message filtering (media, text, etc.)  
✅ Skip duplicate messages  
✅ Skipping specific number of messages  
"""

    HOW_USE_TXT = """<b><u>⚙️ How to Use</u></b>

1. Add this bot or userbot to the source and destination channels.  
2. Give admin permissions in the target channel (bot or userbot must be admin).  
3. If the source is private, the userbot must be a member or admin.  
4. Use <code>/settings</code> to configure source & target chats.  
5. Use <code>/forward</code> to start forwarding messages.

▶️ <a href='https://youtu.be/wO1FE-lf35I'>Watch Tutorial Video</a>"""

    ABOUT_TXT = """<b>
╔═══[ Forward Bot Info ]═══╗
┣⪼ Name: <a href='https://t.me/VJForwardBot'>Forward Bot</a>
┣⪼ Creator: <a href='https://t.me/kingvj01'>King VJ</a>
┣⪼ Updates: <a href='https://t.me/vj_botz'>VJ Botz</a>
┣⪼ Hosted On: Super Fast Server
┣⪼ Language: Python 3
┣⪼ Library: Pyrogram 2.11.0
┣⪼ Version: 0.18.3
╚══════════════════════════╝</b>"""

    STATUS_TXT = """
<b>╔═══[ Bot Status ]═══╗
┣⪼ Uptime: <code>{}</code>
┣⪼ Total Users: <code>{}</code>
┣⪼ Total Bots: <code>{}</code>
┣⪼ Total Forwardings: <code>{}</code>
╚══════════════════════╝</b>
"""

    FROM_MSG = "<b>🔹 Set Source Chat\n\nForward or send the link of the last message from the source channel.\nUse /cancel to stop.</b>"

    TO_MSG = "<b>🔹 Set Target Chat\n\nChoose the destination chat using the inline buttons.\nUse /cancel to stop.</b>"

    SKIP_MSG = "<b>🔹 Set Skip Count</b>\n\nEnter a number of messages to skip before starting forwarding.\nDefault is <code>0</code>.\nExample: 0 = no skip, 5 = skip first 5 messages."

    CANCEL = "<b>❌ Process Cancelled Successfully.</b>"

    BOT_DETAILS = "<b><u>🤖 Bot Details</u></b>\n\n<b>Name:</b> <code>{}</code>\n<b>ID:</b> <code>{}</code>\n<b>Username:</b> @{}"

    USER_DETAILS = "<b><u>👤 Userbot Details</u></b>\n\n<b>Name:</b> <code>{}</code>\n<b>ID:</b> <code>{}</code>\n<b>Username:</b> @{}"

    TEXT = """
<b>╔═══[ Forward Summary ]═══╗
┣⪼ Fetched Messages: <code>{}</code>
┣⪼ Successfully Forwarded: <code>{}</code>
┣⪼ Duplicates Skipped: <code>{}</code>
┣⪼ Deleted: <code>{}</code>
┣⪼ Skipped: <code>{}</code>
┣⪼ Filtered: <code>{}</code>
┣⪼ Current Status: <code>{}</code>
┣⪼ Completion: <code>{}</code>%
╚══════════════════════════╝
<b>Forwarding by {}</b>
"""

    DUPLICATE_TEXT = """
<b>╔═══[ Duplicate Cleaner ]═══╗
┣⪼ Files Scanned: <code>{}</code>
┣⪼ Duplicates Removed: <code>{}</code>
╚══════════════════════════╝
<b>Done by {}</b>
"""

    DOUBLE_CHECK = """<b><u>⚠️ Final Check Before Forwarding</u></b>

<b>Bot:</b> [{botname}](https://t.me/{botuname})  
<b>From Channel:</b> <code>{from_chat}</code>  
<b>To Channel:</b> <code>{to_chat}</code>  
<b>Skip Messages:</b> <code>{skip}</code>

Ensure the bot has admin rights in the target chat.  
If the source is private, your bot or userbot must be a member/admin.

✅ Click <b>YES</b> only if everything is properly set."""

    SETTINGS_TXT = "<b>⚙️ Configure your personal forwarding settings below.</b>"