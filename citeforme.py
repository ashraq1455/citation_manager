from pyrogram import Client, Message, Filters
import requests
import datetime
from bs4 import BeautifulSoup as soup


time = datetime.datetime.now()

API_ID = 
API_HASH = ""
BOT_TOKEN = ""


bot = Client("bot", API_ID, API_HASH, BOT_TOKEN)

def pdf(doi):
    try:
        URL = f"https://scihub.wikicn.top/{doi}"
        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

        req = requests.get(URL, headers=headers)
        html = soup(req.content.decode("utf-8"), "html.parser")

        pdf_link = html.find("iframe", {"id": "pdf"})["src"]
        print(pdf_link)
        return pdf_link

    except Exception as e:
        print(e)
        return "PDF Not Available!"


def cite(doi):
    
    headers = {"Accept": "text/x-bibliography", "style": "harward"}
    r = requests.post(doi, headers=headers)

    full_citation = ""
    for x in r:
        full_citation += x.decode("utf-8")

    final = full_citation.replace("doi:", "Available from: https://doi.org/") + f"[Accessed: {time.day} {time.strftime('%B')} {time.year}]."

    print(final)
    return final


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
        try:
            
            citation = cite(msg)
            if "DOI Not Found" in citation:
                text = "ERROR: DOI Not Found!"
                print(text)
                await bot.send_message(chat_id, text)
            else:
                get_pdf = pdf(msg)
                await bot.send_message(chat_id, get_pdf)
                await bot.send_message(chat_id, citation, disable_web_page_preview=True)

        except Exception as e:
            print(e)
            text = "Citation not available. Make sure your link is correct."
            await bot.send_message(chat_id, text)
    else:
        try:
            doi_link = f"http://doi.org/{msg}"

            citation = cite(doi_link)

            if "DOI Not Found" in citation:
                text = "ERROR: DOI Not Found!"
                print(text)
                await bot.send_message(chat_id, text)
            else:
                
                get_pdf = pdf(msg)
                await bot.send_message(chat_id, get_pdf)
                await bot.send_message(chat_id, citation, disable_web_page_preview=True)
        
        except Exception as e:
            print(e)
            text = "Citation not available. Make sure your link is correct."
            await bot.send_message(chat_id, text)

bot.run()

