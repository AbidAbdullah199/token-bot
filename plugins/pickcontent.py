import random
import time
from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram.errors import FloodWait
import asyncio

# Import your config file or define the channel ID here
from config import CT_CNL_ID

# Store the last request time for each user
user_last_request = {}

@Client.on_message(filters.command("autocontent"))
async def autocontent(client: Client, message: Message):
    user_id = message.from_user.id
    current_time = time.time()

    # Check if the user has made a request in the last 2 seconds
    if user_id in user_last_request and current_time - user_last_request[user_id] < 2:
        wait_time = 2 - (current_time - user_last_request[user_id])
        await message.reply_text(f"Please wait {wait_time:.1f} seconds before requesting again.")
        return

    try:
        # Update the last request time for this user
        user_last_request[user_id] = current_time

        # Get the total number of messages in the channel
        total_messages = await client.get_chat_history_count(CT_CNL_ID)

        if total_messages == 0:
            await message.reply_text("The channel is empty. No content to pick from.")
            return

        # Generate a random message ID
        random_message_id = random.randint(1, total_messages)

        # Fetch the random message
        async for random_message in client.get_chat_history(CT_CNL_ID, limit=1, offset_id=random_message_id):
            # Check if the message has any content
            if random_message.text:
                content = random_message.text
            elif random_message.caption:
                content = random_message.caption
            elif random_message.media:
                # If it's a media message without text, forward it
                await random_message.forward(message.chat.id)
                return
            else:
                content = "This message has no text content."

            # Send the content to the user
            await message.reply_text(f"Here's a random post from the channel:\n\n{content}")
            
            # If the message has media, forward it as well
            if random_message.media:
                await random_message.forward(message.chat.id)

    except FloodWait as e:
        # Handle rate limiting
        await message.reply_text(f"Too many requests. Please try again after {e.x} seconds.")
        await asyncio.sleep(e.x)
    except Exception as e:
        # Handle other exceptions
        await message.reply_text(f"An error occurred: {str(e)}")

# This function will be called to set up the plugin
def setup(app: Client):
    app.add_handler(filters.command("autocontent"), autocontent)
