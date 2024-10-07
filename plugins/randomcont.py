@Client.on_message(filters.command("randomcontent"))
async def random_content(client, message):
    await message.reply_text("Random content command triggered!")  # Debug message
    # Rest of your random content logic
