# bot/plugins/exec.py
import asyncio
from pyrogram import Client, filters
from config import BOT_OWNER

@Client.on_message(filters.command("exec") & filters.private)
async def exec_cmd(client, message):
    # কেবল OWNER এর জন্য
    if message.from_user.id != BOT_OWNER:
        return await message.reply("⛔️ এই কমান্ড শুধু বট মালিকের জন্য!")

    if len(message.text.split()) < 2:
        return await message.reply("⚠️ কোনো কমান্ড দাওনি!")

    command = message.text.split(" ", 1)[1]
    try:
        process = await asyncio.create_subprocess_shell(
            command,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        stdout, stderr = await process.communicate()
        result = (stdout + stderr).decode().strip()

        if not result:
            result = "✅ কমান্ড সফলভাবে রান হয়েছে, কিন্তু কোনো আউটপুট নেই।"

        # বড় আউটপুট কেটে ফেলা
        if len(result) > 4000:
            result = result[:4000] + "\n\n...আউটপুট বড় ছিল, কেটে দেওয়া হয়েছে..."

        await message.reply(f"**Output:**\n```{result}```")

    except Exception as e:
        await message.reply(f"❌ ত্রুটি:\n```{e}```")