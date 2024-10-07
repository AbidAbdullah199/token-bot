import random
from pyrogram import Client, filters
from motor.motor_asyncio import AsyncIOMotorClient
from config import RCHANNEL_ID, DB_URL  # Using DB_URL for MongoDB URI

# Initialize MongoDB client and database
mongo_client = AsyncIOMotorClient(DB_URL)
db = mongo_client["telegram_bot"]
photo_collection = db["photos"]

# Listen for new photo messages in the channel and store their IDs in MongoDB
@Client.on_message(filters.chat(RCHANNEL_ID) & filters.photo)
async def store_photo_in_db(client, message):
    try:
        # Check if the message is already in the database to avoid duplicates
        existing_photo = await photo_collection.find_one({"message_id": message.message_id})
        
        if not existing_photo:
            # Insert the photo message ID and additional info into MongoDB
            await photo_collection.insert_one({
                "message_id": message.message_id,
                "caption": message.caption,  # Optional: Store the caption for reference
                "buttons": message.reply_markup  # Optional: Store buttons for reference
            })
            print(f"Photo message {message.message_id} stored in the database.")
    except Exception as e:
        print(f"Error storing photo in database: {e}")

# Command to forward a random photo message from the channel
@Client.on_message(filters.command("randomcontent"))
async def forward_random_photo_message(client, message):
    try:
        # Fetch all stored photo messages from MongoDB
        photo_messages = await photo_collection.find().to_list(None)
        
        # Check if there are any stored photo messages
        if not photo_messages:
            await message.reply_text("No photo messages found in the channel!")
            return

        # Select a random photo message
        random_photo = random.choice(photo_messages)
        random_message_id = random_photo["message_id"]

        # Forward the selected photo message from the channel to the user
        await client.forward_messages(
            chat_id=message.chat.id,  # User who sent the command
            from_chat_id=RCHANNEL_ID,  # The channel with your photos
            message_ids=random_message_id  # Randomly selected message ID
        )

    except Exception as e:
        # Handle any errors
        await message.reply_text(f"An error occurred: {e}")
