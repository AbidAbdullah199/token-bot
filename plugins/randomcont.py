import random
from pyrogram import Client, filters
from config import RCHANNEL_ID  # Ensure RCHANNEL_ID is properly set in config.py

@Client.on_message(filters.command("randomcontent"))
async def random_content(client, message):
    try:
        # Fetch the most recent 100 messages from the channel
        messages = await client.get_chat_history(chat_id=RCHANNEL_ID, limit=100)

        # Filter only the messages that contain photos
        photo_messages = [msg for msg in messages if msg.photo]

        if not photo_messages:
            await message.reply_text("No photos found in the channel!")
            return

        # Select a random photo message
        random_message = random.choice(photo_messages)

        # Get the caption and buttons (if any)
        caption = random_message.caption if random_message.caption else "Here's a random photo from the channel"
        reply_markup = random_message.reply_markup

        # Send the photo with the caption and buttons
        await client.send_photo(
            chat_id=message.chat.id,
            photo=random_message.photo.file_id,
            caption=caption,
            reply_markup=reply_markup
        )

    except Exception as e:
        await message.reply_text(f"An error occurred: {e}")

