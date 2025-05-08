# bot/plugins/exec.py
import asyncio
from pyrogram import Client, filters
from config import BOT_OWNER

@Client.on_message(filters.command("exec") & filters.user(BOT_OWNER))
async def exec_cmd(_, message):
    if len(message.command) < 2:
        return await message.reply("⚠️ কোনো কমান্ড দেওয়া হয়নি!")

    command = message.text.split(" ", 1)[1]

    try:
        process = await asyncio.create_subprocess_shell(
            command,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        stdout, stderr = await process.communicate()
        result = stdout.decode().strip() + "\n" + stderr.decode().strip()

        if not result.strip():
            result = "✅ কমান্ড সফলভাবে রান হয়েছে, কিন্তু কোনো আউটপুট নেই।"

        if len(result) > 4000:
            result = result[:4000] + "\n\n...আউটপুট বড় ছিল, কেটে দেওয়া হয়েছে..."

        await message.reply(f"**Output:**\n```{result}```")

    except Exception as e:
        await message.reply(f"❌ ত্রুটি:\n```{e}```")