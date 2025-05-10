import os
from config import Config

class  Script(object):
  START_TXT = """<b>ʜɪ {}
  
ɪ'ᴍ ᴀ ᴀᴅᴠᴀɴᴄᴇᴅ ꜰᴏʀᴡᴀʀᴅ ʙᴏᴛ
ɪ ᴄᴀɴ ꜰᴏʀᴡᴀʀᴅ ᴀʟʟ ᴍᴇssᴀɢᴇ ꜰʀᴏᴍ ᴏɴᴇ ᴄʜᴀɴɴᴇʟ ᴛᴏ ᴀɴᴏᴛʜᴇʀ ᴄʜᴀɴɴᴇʟ</b>

**ᴄʟɪᴄᴋ ʜᴇʟᴘ ʙᴜᴛᴛᴏɴ ᴛᴏ ᴋɴᴏᴡ ᴍᴏʀᴇ ᴀʙᴏᴜᴛ ᴍᴇ**"""
  HELP_TXT = """<b><u>🔆 Help</b></u>

<u>**📚 Available commands:**</u>
<b>⏣ __/start - check I'm alive__ 
⏣ __/forward - forward messages__
⏣ __/settings - configure your settings__
⏣ __ /cleandup - delete duplicate media messages in chats__
⏣ __ /stop - stop your ongoing tasks__
⏣ __ /reset - reset your settings__</b>

<b><u>💢 Features:</b></u>
<b>► __Forward message from public channel to your channel without admin permission. if the channel is private need admin permission, if you can't give admin permission then use userbot, but in userbot there is a chance to get your account ban so use fake account__
► __custom caption__
► __custom button__
► __skip duplicate messages__
► __filter type of messages__</b>
"""

  HOW_USE_TXT = """<b><u>⚠️ Before Forwarding:</b></u>
<b>► __add a bot or userbot__
► __add atleast one to channel__ `(your bot/userbot must be admin in there)`
► __You can add chats or bots by using /settings__
► __if the **From Channel** is private your userbot must be member in there or your bot must need admin permission in there also__
► __Then use /forward to forward messages__

► ʜᴏᴡ ᴛᴏ ᴜsᴇ ᴍᴇ [ᴛᴜᴛᴏʀɪᴀʟ ᴠɪᴅᴇᴏ](https://youtu.be/wO1FE-lf35I)</b>"""

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

<i>⚠️ • <a href="https://t.me/{botuname}">{botname}</a> must be an admin in the <b>TARGET CHAT</b></i> <code>({to_chat})</code>

<i>🔒 • If the <b>SOURCE CHAT</b> is private, your userbot must be a member OR your bot must be an admin there too.</i>

━━━━━━━━━━━━━━━━━━━━━━

<b>✅ If both conditions are confirmed, you may now click the "Yes" button to proceed.</b>
"""

SETTINGS_TXT = """<b>change your settings as your wish</b>"""