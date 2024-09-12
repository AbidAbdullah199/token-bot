from aiohttp import web
from plugins import web_server

import pyromod.listen
from pyrogram import Client, filters
from pyrogram.enums import ParseMode
import sys
from datetime import datetime
import random
import time

from config import API_HASH, APP_ID, LOGGER, TG_BOT_TOKEN, TG_BOT_WORKERS, FORCE_SUB_CHANNEL, CHANNEL_ID, PORT, CT_CNL_ID
import pyrogram.utils

pyrogram.utils.MIN_CHAT_ID = -999999999999
pyrogram.utils.MIN_CHANNEL_ID = -100999999999999

class Bot(Client):
    def __init__(self):
        super().__init__(
            name="Bot",
            api_hash=API_HASH,
            api_id=APP_ID,
            plugins={
                "root": "plugins"
            },
            workers=TG_BOT_WORKERS,
            bot_token=TG_BOT_TOKEN
        )
        self.LOGGER = LOGGER
        self.user_last_request = {}

    async def start(self):
        await super().start()
        usr_bot_me = await self.get_me()
        self.uptime = datetime.now()

        if FORCE_SUB_CHANNEL:
            try:
                link = (await self.get_chat(FORCE_SUB_CHANNEL)).invite_link
                if not link:
                    await self.export_chat_invite_link(FORCE_SUB_CHANNEL)
                    link = (await self.get_chat(FORCE_SUB_CHANNEL)).invite_link
                self.invitelink = link
            except Exception as a:
                self.LOGGER(__name__).warning(a)
                self.LOGGER(__name__).warning("Bot can't Export Invite link from Force Sub Channel!")
                self.LOGGER(__name__).warning(f"Please Double check the FORCE_SUB_CHANNEL value and Make sure Bot is Admin in channel with Invite Users via Link Permission, Current Force Sub Channel Value: {FORCE_SUB_CHANNEL}")
                self.LOGGER(__name__).info("\nBot Stopped. Join https://t.me/ultroid_official for support")
                sys.exit()
        try:
            db_channel = await self.get_chat(CHANNEL_ID)
            self.db_channel = db_channel
            test = await self.send_message(chat_id=db_channel.id, text="Test Message")
            await test.delete()
        except Exception as e:
            self.LOGGER(__name__).warning(f"Error occurred: {e}")
            self.LOGGER(__name__).warning(f"CHANNEL_ID: {CHANNEL_ID}, DB Channel ID: {db_channel.id if 'db_channel' in locals() else 'N/A'}")
            self.LOGGER(__name__).warning(f"Make sure bot is Admin in DB Channel, and Double-check the CHANNEL_ID value.")
            self.LOGGER(__name__).info("\nBot Stopped. Join https://t.me/ultroid_official for support")
            sys.exit()

        self.set_parse_mode(ParseMode.HTML)
        self.LOGGER(__name__).info(f"Bot Running..!\n\nCreated by \nhttps://t.me/ultroid_official")
        self.LOGGER(__name__).info(f""" \n\n       
(っ◔◡◔)っ ♥ ULTROIDOFFICIAL ♥
░╚════╝░░╚════╝░╚═════╝░╚══════╝
                                          """)
        self.username = usr_bot_me.username
        #web-response
        app = web.AppRunner(await web_server())
        await app.setup()
        bind_address = "0.0.0.0"
        await web.TCPSite(app, bind_address, PORT).start()

    async def stop(self, *args):
        await super().stop()
        self.LOGGER(__name__).info("Bot stopped.")

    @Client.on_message(filters.command("autocontent"))
    async def autocontent(self, client, message):
        user_id = message.from_user.id
        current_time = time.time()

        # Check if the user has made a request in the last 2 seconds
        if user_id in self.user_last_request and current_time - self.user_last_request[user_id] < 2:
            wait_time = 2 - (current_time - self.user_last_request[user_id])
            await message.reply_text(f"Please wait {wait_time:.1f} seconds before requesting again.")
            return

        try:
            # Update the last request time for this user
            self.user_last_request[user_id] = current_time

            # Get the total number of messages in the channel
            total_messages = await self.get_chat_history_count(CT_CNL_ID)

            if total_messages == 0:
                await message.reply_text("The channel is empty. No content to pick from.")
                return

            # Generate a random message ID
            random_message_id = random.randint(1, total_messages)

            # Fetch the random message
            async for random_message in self.get_chat_history(CT_CNL_ID, limit=1, offset_id=random_message_id):
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

        except Exception as e:
            # Handle other exceptions
            await message.reply_text(f"An error occurred: {str(e)}")
            self.LOGGER(__name__).error(f"Error in autocontent: {str(e)}")
