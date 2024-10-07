import random
from pyrogram import Client, filters
from config import RCHANNEL_ID

@Client.on_message(filters.command("randomcontent"))
async def random_content(client, message):
    try:
        # Fetch the most recent 100 messages from the channel (you can adjust the limit)
        messages = []
        async for msg in client.get_chat_history(chat_id=RCHANNEL_ID, limit=100):
            messages.append(msg)

        # Filter only the messages that contain photos
        photo_messages = [msg for msg in messages if msg.photo]

        if not photo_messages:
            await message.reply_text("No photos found in the channel!")
            return

        # Select a random photo message
        random_message = random.choice(photo_messages)

        # Send the photo with the caption and buttons (without the channel header)
        await client.send_photo(
            chat_id=message.chat.id,
            photo=random_message.photo.file_id,  # Send the same photo
            caption=random_message.caption,  # Use the original caption
            reply_markup=random_message.reply_markup  # Use the original buttons
        )

    except Exception as e:
        # Handle any errors and notify the user
        await message.reply_text(f"An error occurred: {e}")
