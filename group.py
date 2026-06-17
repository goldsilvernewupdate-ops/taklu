from pyrogram import Client, filters
from pyrogram.enums import ChatType
from pyrogram.errors import FloodWait
import asyncio

API_ID = 36725876
API_HASH = "1d72a907b967eacc0811690b38c87e26"
SESSION_NAME = "reply"

app = Client(SESSION_NAME, api_id=API_ID, api_hash=API_HASH)

@app.on_message(filters.command("send", prefixes="/") & filters.me)
async def broadcast_handler(client, message):
    replied = message.reply_to_message

    if not replied:
        await message.edit("❌ Kisi message ya sticker pe reply karo!")
        return

    broadcast_text = " ".join(message.command[1:]) if len(message.command) > 1 else ""

    # Case detect karo
    if replied.sticker:
        mode = "sticker"
        sticker_id = replied.sticker.file_id
    elif replied.text or replied.caption:
        mode = "message"
    else:
        await message.edit("❌ Sirf sticker ya text message pe reply karo!")
        return

    await message.edit("🚀 Broadcasting start ho rahi hai...")

    count = 0
    async for dialog in client.get_dialogs():
        chat = dialog.chat
        if chat.type in [ChatType.GROUP, ChatType.SUPERGROUP]:
            try:
                # Case 1: Sirf sticker
                if mode == "sticker":
                    await client.send_sticker(chat.id, sticker_id)

                # Case 2: Message (text/media) forward
                elif mode == "message":
                    await replied.forward(chat.id)

                await asyncio.sleep(1)

                # Dono cases mein extra text bhejo agar diya ho
                if broadcast_text:
                    await client.send_message(chat.id, broadcast_text)

                count += 1
                await asyncio.sleep(3)

            except FloodWait as e:
                await asyncio.sleep(e.value)
            except Exception as e:
                print(f"Error in {chat.title}: {e}")

    await message.edit(f"✅ Done! {count} groups mein send ho gaya.")

app.run()
