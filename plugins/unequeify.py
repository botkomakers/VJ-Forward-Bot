#তথদ

from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from config import Config
from database import db

@Client.on_message(filters.command("mongclear") & filters.user(Config.BOT_OWNER))
async def mong_clear_handler(client: Client, message: Message):
    keyboard = InlineKeyboardMarkup(
        [[
            InlineKeyboardButton("✅ Confirm Delete", callback_data="confirm_mong_clear"),
            InlineKeyboardButton("❌ Cancel", callback_data="cancel_mong_clear")
        ]]
    )
    await message.reply_text(
        "**⚠️ Are you sure you want to delete all MongoDB data?**\n\n"
        "This will wipe all collections (`users`, `bots`, `userbot`, `notify`, `channels`).\n\n"
        "Press **Confirm Delete** only if you are sure!",
        reply_markup=keyboard
    )


@Client.on_callback_query(filters.regex("^(confirm_mong_clear|cancel_mong_clear)$"))
async def confirm_clear_callback(client, callback_query):
    if callback_query.from_user.id != Config.BOT_OWNER:
        return await callback_query.answer("Access denied!", show_alert=True)

    if callback_query.data == "cancel_mong_clear":
        return await callback_query.edit_message_text("❌ MongoDB wipe canceled.")

    try:
        await db.col.drop()
        await db.bot.drop()
        await db.userbot.drop()
        await db.nfy.drop()
        await db.chl.drop()

        await callback_query.edit_message_text("✅ All MongoDB collections have been successfully deleted!")
    except Exception as e:
        await callback_query.edit_message_text(f"❌ Error while clearing MongoDB: `{e}`")