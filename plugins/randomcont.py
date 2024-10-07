import random
from pyrogram import Client, filters
from config import RCHANNEL_ID  # Import RCHANNEL_ID from config.py

# Define the bot command /randomcontent
@Client.on_message(filters.command("randomcontent"))
async def random_content(client, message):
    try:
        # Get the total number of messages in the channel
        channel_info = await client.get_chat(RCHANNEL_ID)
        total_messages = channel_info.message_count

        while True:
            # Select a random message number
            random_message_id = random.randint(1, total_messages)

            # Fetch the random message
            random_message = await client.get_messages(chat_id=RCHANNEL_ID, message_ids=random_message_id)

            # Check if the message contains a photo
            if random_message.photo:
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
                break  # Exit the loop once a valid photo post is found

    except Exception as e:
        await message.reply_text(f"An error occurred: {e}")
