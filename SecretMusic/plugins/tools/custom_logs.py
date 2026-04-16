import random
from pyrogram import filters, enums
from pyrogram.types import Message
from config import LOG_GROUP_ID, SUDOERS
from SecretMusic import app
from SecretMusic.utils.database.logdatabase import get_log_messages, set_log_message, reset_log_messages
from SecretMusic.misc import SUDOERS as SUDO_USERS

LOG_IMAGE = "https://i.ibb.co/vvkm3C0j/IMG-20260415-021910-937.jpg"

@app.on_message(filters.command(["setlogwelcome", "setlogleft", "setlogdm"]) & filters.user(SUDO_USERS))
async def set_logs(_, message: Message):
    if len(message.command) < 2:
        return await message.reply_text("<b>❖ ᴜsᴀɢᴇ ➥</b> /setlog[type] [message]\n\n<b>Types:</b> welcome, left, dm\n<b>Placeholders:</b> {mention}, {id}, {username}, {chat_name}, {chat_id}")
    
    cmd = message.command[0].lower()
    log_type = cmd.replace("setlog", "")
    new_msg = message.text.split(None, 1)[1]
    
    await set_log_message(log_type, new_msg)
    await message.reply_text(f"✅ <b>Custom {log_type} log message updated!</b>")

@app.on_message(filters.command("resetlogs") & filters.user(SUDO_USERS))
async def reset_logs(_, message: Message):
    await reset_log_messages()
    await message.reply_text("✅ <b>All log messages reset to default!</b>")

# Listener for Group Joins (When Bot is added)
@app.on_message(filters.new_chat_members, group=10)
async def log_group_join(_, message: Message):
    for member in message.new_chat_members:
        if member.id == app.id:
            logs = await get_log_messages()
            template = logs.get("welcome")
            
            chat_name = message.chat.title
            chat_id = message.chat.id
            mention = message.from_user.mention
            user_id = message.from_user.id
            
            log_text = template.format(
                chat_name=chat_name,
                chat_id=chat_id,
                mention=mention,
                user_id=user_id,
                username=message.from_user.username or "ɴ/ᴀ"
            )
            
            await app.send_photo(LOG_GROUP_ID, photo=LOG_IMAGE, caption=log_text)

# Listener for Group Left (When Bot is removed)
@app.on_message(filters.left_chat_member, group=12)
async def log_group_left(_, message: Message):
    if message.left_chat_member.id == app.id:
        logs = await get_log_messages()
        template = logs.get("left")
        
        chat_name = message.chat.title
        chat_id = message.chat.id
        mention = message.from_user.mention if message.from_user else "𝐔ɴᴋɴᴏᴡɴ 𝐔sᴇʀ"
        user_id = message.from_user.id if message.from_user else "0000"
        
        log_text = template.format(
            chat_name=chat_name,
            chat_id=chat_id,
            mention=mention,
            user_id=user_id,
            username=message.from_user.username if message.from_user else "ɴ/ᴀ"
        )
        
        await app.send_photo(LOG_GROUP_ID, photo=LOG_IMAGE, caption=log_text)

# Listener for DM Start
@app.on_message(filters.private & filters.command("start"), group=11)
async def log_dm_start(_, message: Message):
    # Only log once if user is new (handled by database usually, but we log every /start for safety)
    logs = await get_log_messages()
    template = logs.get("dm")
    
    mention = message.from_user.mention
    user_id = message.from_user.id
    username = message.from_user.username or "ɴᴏ_ᴜsᴇʀɴᴀᴍᴇ"
    
    log_text = template.format(
        mention=mention,
        user_id=user_id,
        username=username,
        chat_name="Private",
        chat_id=user_id
    )
    
    # We use a separate group group check or flag to avoid spamming if needed, 
    # but here we log as requested.
    await app.send_photo(LOG_GROUP_ID, photo=LOG_IMAGE, caption=log_text)
