import random
from pyrogram import Client, filters
from config import RCHANNEL_ID  # Your channel ID where posts are coming from

# Cache to store photo messages with captions and buttons
photo_messages_cache = []

# This function listens for new messages in the channel and stores photo messages with captions and buttons
@Client.on_message(filters.chat(RCHANNEL_ID) & filters.photo)
async def store_photo_message(client, message):
    # Store photo messages that have captions and buttons
    if message.caption and message.reply_markup:  # Ensure the message has a caption and buttons
        photo_messages_cache.append(message)

        # Optional: Limit the cache size to avoid memory issues
        if len(photo_messages_cache) > 100:
            photo_messages_cache.pop(0)  # Remove the oldest message when the cache is full

# Command to forward a random photo message from the channel to the user
@Client.on_message(filters.command("randomcontent"))
async def forward_random_photo_message(client, message):
    try:
        # Check if there are any photo messages in the cache
        if not photo_messages_cache:
            await message.reply_text("No photo messages with captions and buttons found in the channel!")
            return

        # Select a random photo message from the cache
        random_message = random.choice(photo_messages_cache)

        # Forward the random photo message to the user who triggered the command
        await random_message.forward(chat_id=message.chat.id)

    except Exception as e:
        # Handle any errors
        await message.reply_text(f"An error occurred: {e}")
