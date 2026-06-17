from pyrogram import Client, filters
from pyrogram.enums import ChatType
from pyrogram.errors import FloodWait
import asyncio

app = Client("reply")

@app.on_message(filters.command("send", prefixes="/") & filters.me)
async def broadcast_handler(client, message):
    replied = message.reply_to_message

    if not replied:
        await message.edit("❌ Kisi message ya sticker pe reply karo!")
        return

    broadcast_text = " ".join(message.command[1:]) if len(message.command) > 1 else ""

    if replied.sticker:
        mode = "sticker"
        sticker_id = replied.sticker.file_id
    elif replied.text or replied.photo or replied.video or replied.document or replied.audio or replied.caption:
        mode = "message"
    else:
        await message.edit("❌ Supported type nahi hai!")
        return

    await message.edit("🚀 Broadcasting start ho rahi hai...")

    count = 0
    async for dialog in client.get_dialogs():
        chat = dialog.chat
        if chat.type in [ChatType.GROUP, ChatType.SUPERGROUP]:
            try:
                if mode == "sticker":
                    await client.send_sticker(chat.id, sticker_id)

                elif mode == "message":
                    if replied.text:
                        await client.send_message(chat.id, replied.text)
                    elif replied.photo:
                        await client.send_photo(chat.id, replied.photo.file_id, caption=replied.caption or "")
                    elif replied.video:
                        await client.send_video(chat.id, replied.video.file_id, caption=replied.caption or "")
                    elif replied.document:
                        await client.send_document(chat.id, replied.document.file_id, caption=replied.caption or "")
                    elif replied.audio:
                        await client.send_audio(chat.id, replied.audio.file_id, caption=replied.caption or "")

                await asyncio.sleep(1)

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
