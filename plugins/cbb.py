#(©)Codexbotz

from pyrogram import __version__
from bot import Bot
from config import OWNER_ID
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery

@Bot.on_callback_query()
async def cb_handler(client: Bot, query: CallbackQuery):
    data = query.data
    if data == "about":
        await query.message.edit_text(
            text = f"<b>○ Oᴡɴᴇʀ : <a href='tg://user?id={OWNER_ID}'>D Lᴜғғʏ</a>\n○ Cʜᴀɴɴᴇʟ : <a href='https://t.me/AnimeQuestX'>Aɴɪᴍᴇ Qᴜᴇsᴛ</a>○ Oɴɢᴏɪɴɢ Cʜᴀɴɴᴇʟ : <a href='https://OngoingAnimeQuest'>Jᴏɪɴ Nᴏᴡ</a>\n○ Dɪsᴄᴜssɪᴛᴏɴ Cʜᴀɴɴᴇʟ : <a href='https://t.me/+r-x-wA4JT5gxZjVl'>Jᴏɪɴ Nᴏᴡ</a>\n○ Mᴀɴɢᴀ Cʜᴀɴɴᴇʟ : <a>href'https://t.me/AnimeQuestManga'>Jᴏɪɴ Nᴏᴡ</a>\n○ Hɪɴᴅɪ Cʜᴀɴɴᴇʟ : <a href'https://t.me/AnimeQuestHindi'>Join Now</a></b>",
            disable_web_page_preview = True,
            reply_markup = InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton("🔒 Close", callback_data = "close")
                    ]
                ]
            )
        )
    elif data == "close":
        await query.message.delete()
        try:
            await query.message.reply_to_message.delete()
        except:
            pass
