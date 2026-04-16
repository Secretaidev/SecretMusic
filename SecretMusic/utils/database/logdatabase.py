from SecretMusic.core.mongo import mongodb

logdb = mongodb.logsettings

async def get_log_messages():
    res = await logdb.find_one({"id": "log_strings"})
    if not res:
        return {
            "welcome": "✫ <b><u>#𝐍ᴇᴡ_𝐆ʀᴏᴜᴘ_𝐀ᴅᴅᴇᴅ</u></b> ✫\n\n<b>𝐂ʜᴀᴛ 𝐓ɪᴛʟᴇ :</b> {chat_name}\n<b>𝐂ʜᴀᴛ 𝐈ᴅ :</b> <code>{chat_id}</code>\n<b>𝐀ᴅᴅᴇᴅ 𝐁ʏ :</b> {mention} (<code>{user_id}</code>)",
            "left": "✫ <b><u>#𝐋ᴇғᴛ_𝐆ʀᴏᴜᴘ</u></b> ✫\n\n<b>𝐂ʜᴀᴛ 𝐓ɪᴛʟᴇ :</b> {chat_name}\n<b>𝐂ʜᴀᴛ 𝐈ᴅ :</b> <code>{chat_id}</code>\n<b>𝐑ᴇᴍᴏᴠᴇᴅ 𝐁ʏ :</b> {mention} (<code>{user_id}</code>)",
            "dm": "✫ <b><u>#𝐍ᴇᴡ_𝐔sᴇʀ_𝐈ɴ_𝐃𝐌</u></b> ✫\n\n<b>𝐍ᴀᴍᴇ :</b> {mention}\n<b>𝐈ᴅ :</b> <code>{user_id}</code>\n<b>𝐔sᴇʀɴᴀᴍᴇ :</b> @{username}"
        }
    return res

async def set_log_message(type, message):
    await logdb.update_one(
        {"id": "log_strings"},
        {"$set": {type: message}},
        upsert=True
    )

async def reset_log_messages():
    await logdb.delete_one({"id": "log_strings"})
