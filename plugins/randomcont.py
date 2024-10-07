import random
from pyrogram import Client, filters
from config import RCHANNEL_ID  # Ensure RCHANNEL_ID is defined in config.py

@Client.on_message(filters.command("randomcontent", prefixes="/"))
async def random_content(client, message):
    try:
        # Initialize a list to store the messages
        messages = []
        
        # Fetch the most recent 100 messages using async for loop
        async for msg in client.get_chat_history(chat_id=RCHANNEL_ID, limit=100):
            messages.append(msg)
        
        # Filter only the messages that contain photos
        photo_messages = [msg for msg in messages if msg.photo]
        
        # Check if there are any photo messages
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
