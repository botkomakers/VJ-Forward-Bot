import os
from config import Config

class  Script(object):
  START_TXT = """
<b>👋 Hello, {}!</b>

🤖 I’m an <b>Advanced Forward Bot</b> — built to help you seamlessly forward messages from one Telegram channel to another with ease and speed.

<b>💡 Tip:</b> Use the buttons below to get started or click <b>Help</b> to learn more about how I work.
"""
  HELP_TXT = """
<b><u>🔆 Help</u></b>

<u>📚 <b>Available Commands:</b></u>
<b>⏣ /start</b> — Check if I'm alive
<b>⏣ /forward</b> — Forward messages
<b>⏣ /settings</b> — Configure your settings
<b>⏣ /cleandup</b> — Delete duplicate media messages in chats
<b>⏣ /stop</b> — Stop your ongoing tasks
<b>⏣ /reset</b> — Reset your settings

<u>💢 <b>Features:</b></u>
<b>► Forward messages from public channels to your channel without admin permission. 
    For private channels, admin permission is needed. If you can't give admin access, use a userbot (though this could risk account bans, so be careful and consider using a fake account).
► Custom caption
► Custom button
► Skip duplicate messages
► Filter types of messages</b>
"""

  HOW_USE_TXT = """
<b><u>⚠️ Before Forwarding:</u></b>

<b>► Add a bot or userbot to your chat.</b>
<b>► Add at least one channel to the bot/userbot (your bot/userbot must be admin in that channel).</b>
<b>► Use /settings to add chats or bots to your setup.</b>
<b>► If the <u>From Channel</u> is private, your userbot must be a member there, or your bot must be admin in that channel.</b>
<b>► Then use /forward to forward messages.</b>

<b>🎥 ʜᴏᴡ ᴛᴏ ᴜsᴇ ᴍᴇ: [Tutorial Video](https://youtu.be/wO1FE-lf35I)</b>
"""

  ABOUT_TXT = """<b>
╔════❰ ғᴏʀᴡᴀʀᴅ ʙᴏᴛ ❱═❍⊱❁۪۪
║╭━━━━━━━━━━━━━━━➣
║┣⪼📃ʙᴏᴛ : [Fᴏʀᴡᴀᴅ Bᴏᴛ](https://t.me/VJForwardBot)
║┣⪼👦Cʀᴇᴀᴛᴏʀ : [Kɪɴɢ VJ 👑](https://t.me/movie_channel8)
║┣⪼🤖Uᴘᴅᴀᴛᴇ : [VJ Bᴏᴛᴢ](https://t.me/movie_channel8)
║┣⪼📡Hᴏsᴛᴇᴅ ᴏɴ : Sᴜᴘᴇʀ Fᴀsᴛ
║┣⪼🗣️Lᴀɴɢᴜᴀɢᴇ : Pʏᴛʜᴏɴ3
║┣⪼📚Lɪʙʀᴀʀʏ : Pʏʀᴏɢʀᴀᴍ Gᴀᴛʜᴇʀ 2.11.0 
║┣⪼🗒️Vᴇʀsɪᴏɴ : 0.18.3
║╰━━━━━━━━━━━━━━━➣
╚══════════════════❍⊱❁۪۪
</b>"""
  STATUS_TXT = """
╔════❰ ʙᴏᴛ sᴛᴀᴛᴜs  ❱═❍⊱❁۪۪
║╭━━━━━━━━━━━━━━━➣
║┣⪼**⏳ ʙᴏᴛ ᴜᴘᴛɪᴍᴇ:**`{}`
║┃
║┣⪼**👱 Tᴏᴛᴀʟ Usᴇʀs:** `{}`
║┃
║┣⪼**🤖 Tᴏᴛᴀʟ Bᴏᴛ:** `{}`
║┃
║┣⪼**🔃 Fᴏʀᴡᴀʀᴅɪɴɢs:** `{}`
║┃
║╰━━━━━━━━━━━━━━━➣
╚══════════════════❍⊱❁۪۪
"""
  FROM_MSG = """
<b>📥 ❪ SET SOURCE CHAT ❫</b>

<i>🔹 Please forward the <u>last message</u> or paste the <u>message link</u> from the source chat.</i>

<b>✖️ /cancel</b> — to cancel this process at any time.
"""
  TO_MSG = """
<b>📤 ❪ CHOOSE TARGET CHAT ❫</b>

<i>🔹 Please select your <u>target chat</u> from the available buttons below.</i>

<b>✖️ /cancel</b> — to cancel this process anytime.
"""
  SKIP_MSG = """
<b>⏭️ ❪ SET MESSAGE SKIP COUNT ❫</b>

<i>Enter the number of messages you want to skip.</i>
Messages will be skipped from the start, and the rest will be forwarded.

<b>🔢 Default Skip Number:</b> <code>0</code>

<code>• You enter 0 = No messages skipped
• You enter 5 = First 5 messages skipped</code>

<b>✖️ /cancel</b> — to cancel this process anytime.
"""
  CANCEL = "<b>❌ Process Cancelled Successfully!</b>"
  BOT_DETAILS = """
<b><u>🤖 BOT DETAILS</u></b>

<b>➤ Name:</b> <code>{}</code>
<b>➤ Bot ID:</b> <code>{}</code>
<b>➤ Username:</b> <a href="https://t.me/{}">@{}</a>
"""
  USER_DETAILS = """
<b><u>👤 USERBOT DETAILS</u></b>

<b>➤ Name:</b> <code>{}</code>
<b>➤ User ID:</b> <code>{}</code>
<b>➤ Username:</b> <a href="https://t.me/{}">@{}</a>
"""  

  TEXT = """
┏━━━━━━━━━━━━━━━━━━━━━┓
┃   🛰 FORWARD Status   •
┣━━━━━━━━━━━━━━━━━━━━━┫
┃ 🕵️‍♂️  Fetched    : <code>{}</code>
•
┃ ✅  Forwarded   : <code>{}</code>
•
┃ 👥  Duplicates  : <code>{}</code>
•
┃ 🗑  Deleted     : <code>{}</code>
•
┃ 🪆  Skipped     : <code>{}</code>
•
┃ 🔁  Filtered    : <code>{}</code>
•
┃ 📊  Status      : <code>{}</code>
•
┃ 𖨠  Progress    : <code>{}</code>%
•
┗━━━ Tag: <b>{}</b> ━━━┛
"""
  DUPLICATE_TEXT = """
╔════❰ ᴜɴᴇǫᴜɪғʏ sᴛᴀᴛᴜs ❱═❍⊱❁۪۪
║╭━━━━━━━━━━━━━━━➣
║┣⪼ <b>ғᴇᴛᴄʜᴇᴅ ғɪʟᴇs:</b> <code>{}</code>
║┃
║┣⪼ <b>ᴅᴜᴘʟɪᴄᴀᴛᴇ ᴅᴇʟᴇᴛᴇᴅ:</b> <code>{}</code> 
║╰━━━━━━━━━━━━━━━➣
╚════❰ {} ❱══❍⊱❁۪۪
"""
  DOUBLE_CHECK = """
<b>⚠️ <u>DOUBLE CHECKING REQUIRED</u> ⚠️</b>

<code>Before forwarding the messages, please verify the following details carefully.
Click 'Yes' only if everything looks correct:</code>

━━━━━━━━━━━━━━━━━━━━━━
<b>🤖 BOT NAME:</b> <a href="https://t.me/{botuname}">{botname}</a>
<b>📤 FROM CHANNEL:</b> <code>{from_chat}</code>
<b>📥 TO CHANNEL:</b> <code>{to_chat}</code>
<b>🪄 SKIP MESSAGES:</b> <code>{skip}</code>
━━━━━━━━━━━━━━━━━━━━━━

<b>✅ All set? Click the button below to proceed.</b>
"""

<i>° [{botname}](t.me/{botuname}) must be admin in **TARGET CHAT**</i> (`{to_chat}`)
<i>° If the **SOURCE CHAT** is private your userbot must be member or your bot must be admin in there also</b></i>

<b>If the above is checked then the yes button can be clicked</b>"""
"""

SETTINGS_TXT = """<b>change your settings as your wish</b>"""