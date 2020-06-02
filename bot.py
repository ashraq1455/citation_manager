from pyrogram import Client, Message, Filters
import requests
import datetime
from data import get_cite, get_pdf, get_intext
from bs4 import BeautifulSoup as soup

time = datetime.datetime.now()

API_ID = 
API_HASH = ""
BOT_TOKEN = ""

bot = Client("bot", API_ID, API_HASH, BOT_TOKEN)

@bot.on_message(Filters.command("start", prefixes=['/']))
async def create_user_profile(bot: bot, msg: Message):
    chat_id = msg.chat.id
    print(chat_id)
    first_name = msg.chat.first_name
    await bot.send_message(chat_id, "Send a DOI number or a DOI link for Harward style citation.")

@bot.on_message()
async def my_function(client, message): 
    chat_id = message.chat.id
    msg = message["text"]
    print(msg)
    if "doi.org" in msg:
        msg = msg.replace("https://doi.org/", "").replace("doi.org/", "")
        try:
            citation = await get_cite(msg)
            if not citation:
                text = "ERROR: DOI Not Found!"
                print(text)
                await bot.send_message(chat_id, text)
            else:
                get_pdf = await get_pdf(msg)
                in_text  = await get_intext(msg)
                await bot.send_message(chat_id, get_pdf)
                await bot.send_message(chat_id, citation, disable_web_page_preview=True)
                await bot.send_message(chat_id, in_text, disable_web_page_preview=True)
        except Exception as e:
            print(e)
            text = "Citation not available. Make sure your link is correct."
            await bot.send_message(chat_id, text)
    else:
        try:
            citation = await get_cite(msg)
            if not citation:
                text = "ERROR: DOI Not Found!"
                print(text)
                await bot.send_message(chat_id, text)
            else:
                get_pdf = await get_pdf(msg)
                in_text  = await get_intext(msg)
                await bot.send_message(chat_id, get_pdf)
                await bot.send_message(chat_id, citation, disable_web_page_preview=True)
                await bot.send_message(chat_id, in_text, disable_web_page_preview=True)
        except Exception as e:
            print(e)
            text = "Citation not available. Make sure your link is correct."
            await bot.send_message(chat_id, text)
bot.run()

