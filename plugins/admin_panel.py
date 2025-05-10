from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message
from config import Config
from database import db
from pyrogram.enums import ChatAction

ADMIN_USERS = [Config.BOT_OWNER]
BROADCAST_USER_STATE = {}
BAN_STATE = {}
UNBAN_STATE = {}

def is_admin(user_id):
    return user_id in ADMIN_USERS

@Client.on_message(filters.command("admin") & filters.user(ADMIN_USERS))
async def admin_panel(_, message: Message):
    btn = [
        [InlineKeyboardButton("More Options", callback_data="more_options")]
    ]
    await message.reply("**Welcome to Admin Panel**", reply_markup=InlineKeyboardMarkup(btn))

@Client.on_callback_query(filters.regex("more_options") & filters.user(ADMIN_USERS))
async def more_options_handler(_, query):
    btn = [
        [InlineKeyboardButton("Broadcast to User", callback_data="broadcast_user_manual")],
        [InlineKeyboardButton("Ban User", callback_data="ban_user_manual")],
        [InlineKeyboardButton("Unban User", callback_data="unban_user_manual")],
        [InlineKeyboardButton("Back", callback_data="admin_back")]
    ]
    await query.message.edit("**Select an Option:**", reply_markup=InlineKeyboardMarkup(btn))

@Client.on_callback_query(filters.regex("admin_back") & filters.user(ADMIN_USERS))
async def back_admin_menu(_, query):
    btn = [
        [InlineKeyboardButton("More Options", callback_data="more_options")]
    ]
    await query.message.edit("**Welcome to Admin Panel**", reply_markup=InlineKeyboardMarkup(btn))

# Broadcast to specific user
@Client.on_callback_query(filters.regex("broadcast_user_manual") & filters.user(ADMIN_USERS))
async def ask_broadcast_user(_, query):
    await query.message.reply("**Send the User ID to whom you want to forward a message.**")
    BROADCAST_USER_STATE[query.from_user.id] = "awaiting_id"

@Client.on_message(filters.text & filters.user(ADMIN_USERS))
async def handle_broadcast_user_and_ban(_, message: Message):
    user_id = message.from_user.id
    if BROADCAST_USER_STATE.get(user_id) == "awaiting_id":
        try:
            target_id = int(message.text)
            BROADCAST_USER_STATE[user_id] = target_id
            await message.reply("**Now reply to any message you want to forward to that user.**")
        except ValueError:
            await message.reply("Invalid user ID. Please send a numeric ID.")
        return

    elif isinstance(BROADCAST_USER_STATE.get(user_id), int) and message.reply_to_message:
        target_id = BROADCAST_USER_STATE[user_id]
        try:
            await _.copy_message(chat_id=target_id, from_chat_id=message.chat.id, message_id=message.reply_to_message.id)
            await message.reply(f"**Message forwarded to user `{target_id}` successfully.**")
        except Exception as e:
            await message.reply(f"Failed to forward: `{e}`")
        del BROADCAST_USER_STATE[user_id]
        return

    # Ban user flow
    if BAN_STATE.get(user_id) == "awaiting_id":
        try:
            target_id = int(message.text)
            await db.ban_user(target_id)
            await message.reply(f"User `{target_id}` has been **banned**.")
        except Exception as e:
            await message.reply(f"Failed to ban user: `{e}`")
        BAN_STATE.pop(user_id, None)
        return

    # Unban user flow
    if UNBAN_STATE.get(user_id) == "awaiting_id":
        try:
            target_id = int(message.text)
            await db.remove_ban(target_id)
            await message.reply(f"User `{target_id}` has been **unbanned**.")
        except Exception as e:
            await message.reply(f"Failed to unban user: `{e}`")
        UNBAN_STATE.pop(user_id, None)
        return

# Ban User
@Client.on_callback_query(filters.regex("ban_user_manual") & filters.user(ADMIN_USERS))
async def ask_ban_user(_, query):
    await query.message.reply("**Send the User ID you want to ban.**")
    BAN_STATE[query.from_user.id] = "awaiting_id"

# Unban User
@Client.on_callback_query(filters.regex("unban_user_manual") & filters.user(ADMIN_USERS))
async def ask_unban_user(_, query):
    await query.message.reply("**Send the User ID you want to unban.**")
    UNBAN_STATE[query.from_user.id] = "awaiting_id"

# Shortcut command version: /broadcast_user 123456
@Client.on_message(filters.command("broadcast_user") & filters.user(ADMIN_USERS))
async def shortcut_broadcast_user(_, message: Message):
    if len(message.command) < 2 or not message.reply_to_message:
        await message.reply("Usage: `/broadcast_user user_id` (as reply to a message)", quote=True)
        return
    try:
        user_id = int(message.command[1])
        await _.copy_message(chat_id=user_id, from_chat_id=message.chat.id, message_id=message.reply_to_message.id)
        await message.reply(f"Message forwarded to user `{user_id}` successfully.")
    except Exception as e:
        await message.reply(f"Failed to forward: `{e}`")