import random
from pyrogram import filters, enums
from pyrogram.types import Message
from config import LOG_GROUP_ID
from SecretMusic import app
from SecretMusic.utils.database import add_served_chat, get_assistant, delete_served_chat
from SecretMusic.utils.database.logdatabase import get_log_messages, set_log_message, reset_log_messages
from SecretMusic.misc import SUDOERS

LOG_IMAGE = "https://i.ibb.co/vvkm3C0j/IMG-20260415-021910-937.jpg"


@app.on_message(filters.command(["setlogwelcome", "setlogleft", "setlogdm"]) & SUDOERS)
async def set_logs(_, message: Message):
    if len(message.command) < 2:
        return await message.reply_text(
            "<b>❖ ᴜsᴀɢᴇ ➥</b> /setlog[type] [message]\n\n"
            "<b>Types:</b> welcome, left, dm\n"
            "<b>Placeholders:</b> {mention}, {user_id}, {username}, {chat_name}, {chat_id}"
        )
    cmd = message.command[0].lower()
    log_type = cmd.replace("setlog", "")
    new_msg = message.text.split(None, 1)[1]
    await set_log_message(log_type, new_msg)
    await message.reply_text(f"✅ <b>Custom {log_type} log message updated!</b>")


@app.on_message(filters.command("resetlogs") & SUDOERS)
async def reset_logs(_, message: Message):
    await reset_log_messages()
    await message.reply_text("✅ <b>All log messages reset to default!</b>")


# ── Group Join Logger (Bot added to new group) ──
@app.on_message(filters.new_chat_members, group=-10)
async def log_group_join(_, message: Message):
    try:
        for member in message.new_chat_members:
            if member.id == app.id:
                userbot = await get_assistant(message.chat.id)
                count = await app.get_chat_members_count(message.chat.id)
                username = message.chat.username or ""

                logs = await get_log_messages()
                template = logs.get("welcome", "Bot added to {chat_name}")

                try:
                    log_text = template.format(
                        chat_name=message.chat.title,
                        chat_id=message.chat.id,
                        mention=message.from_user.mention if message.from_user else "Unknown",
                        user_id=message.from_user.id if message.from_user else 0,
                        username=message.from_user.username if message.from_user else "N/A",
                        count=count,
                    )
                except (KeyError, IndexError):
                    log_text = (
                        f"✫ <b><u>#𝐍ᴇᴡ_𝐆ʀᴏᴜᴘ</u></b> ✫\n\n"
                        f"<b>𝐂ʜᴀᴛ :</b> {message.chat.title}\n"
                        f"<b>𝐈ᴅ :</b> <code>{message.chat.id}</code>\n"
                        f"<b>𝐌ᴇᴍʙᴇʀs :</b> {count}"
                    )

                try:
                    await app.send_photo(LOG_GROUP_ID, photo=LOG_IMAGE, caption=log_text)
                except Exception:
                    await app.send_message(LOG_GROUP_ID, text=log_text)

                await add_served_chat(message.chat.id)
                if username:
                    try:
                        await userbot.join_chat(f"@{username}")
                    except Exception:
                        pass
    except Exception as e:
        print(f"[custom_logs] join error: {e}")


# ── Group Left Logger (Bot removed from group) ──
@app.on_message(filters.left_chat_member, group=-12)
async def log_group_left(_, message: Message):
    try:
        left = message.left_chat_member
        if not left or left.id != app.id:
            return

        userbot = await get_assistant(message.chat.id)
        logs = await get_log_messages()
        template = logs.get("left", "Bot removed from {chat_name}")

        try:
            log_text = template.format(
                chat_name=message.chat.title,
                chat_id=message.chat.id,
                mention=message.from_user.mention if message.from_user else "Unknown",
                user_id=message.from_user.id if message.from_user else 0,
                username=message.from_user.username if message.from_user else "N/A",
            )
        except (KeyError, IndexError):
            log_text = (
                f"✫ <b><u>#𝐋ᴇғᴛ_𝐆ʀᴏᴜᴘ</u></b> ✫\n\n"
                f"<b>𝐂ʜᴀᴛ :</b> {message.chat.title}\n"
                f"<b>𝐈ᴅ :</b> <code>{message.chat.id}</code>"
            )

        try:
            await app.send_photo(LOG_GROUP_ID, photo=LOG_IMAGE, caption=log_text)
        except Exception:
            await app.send_message(LOG_GROUP_ID, text=log_text)

        await delete_served_chat(message.chat.id)
        try:
            await userbot.leave_chat(message.chat.id)
        except Exception:
            pass
    except Exception as e:
        print(f"[custom_logs] left error: {e}")


# ── DM Start Logger ──
@app.on_message(filters.private & filters.command("start"), group=11)
async def log_dm_start(_, message: Message):
    try:
        logs = await get_log_messages()
        template = logs.get("dm", "New DM from {mention}")

        try:
            log_text = template.format(
                mention=message.from_user.mention,
                user_id=message.from_user.id,
                username=message.from_user.username or "ɴᴏ_ᴜsᴇʀɴᴀᴍᴇ",
                chat_name="Private",
                chat_id=message.from_user.id,
            )
        except (KeyError, IndexError):
            log_text = (
                f"✫ <b>#𝐃𝐌</b> ✫\n\n"
                f"<b>𝐔sᴇʀ :</b> {message.from_user.mention}\n"
                f"<b>𝐈ᴅ :</b> <code>{message.from_user.id}</code>"
            )

        try:
            await app.send_photo(LOG_GROUP_ID, photo=LOG_IMAGE, caption=log_text)
        except Exception:
            await app.send_message(LOG_GROUP_ID, text=log_text)
    except Exception:
        pass
