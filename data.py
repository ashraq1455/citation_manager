import asyncio
import aiohttp
import datetime

from bs4 import BeautifulSoup

p_headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
a_headers = {"Accept": "application/rdf+xml;q=0.5, application/vnd.citationstyles.csl+json;q=1.0"}
c_headers = {"Accept": "text/x-bibliography; style=harvard-staffordshire-university; locale=en-GB"}

async def get_pdf(doi):
    try:
        url = f"https://scihub.wikicn.top/{doi}"
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=p_headers) as res:
                content = await res.text()

        soup = BeautifulSoup(content, "html.parser")
        pdf_link = soup.find("iframe", {"id": "pdf"})["src"]
        print(pdf_link)
        return pdf_link

    except Exception as e:
        print(e)
        return None


async def get_authors(doi):
    url = f"https://doi.org/{doi}"
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=a_headers) as res:
            response = await res.json()
    authors = response['author']
    return authors

async def get_title(doi):
    url = f"https://doi.org/{doi}"
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=a_headers) as res:
            response = await res.json()
    journal_title = response['container-title']
    return journal_title


async def get_cite(doi):
    time = datetime.datetime.now()
    url = f"https://doi.org/{doi}"
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=c_headers) as res:
                citation = await res.text(encoding="utf-8")
            citation = citation[:citation.index(").")].replace("&", "and") + citation[citation.index(")."):]
            citation = citation.strip()[:-1] + f" [Accessed On: {time.day} {time.strftime('%B')} {time.year}]."
            journal_title = await get_title(doi)
            citation = citation.replace(str(journal_title), f"<i>{journal_title}</i>")
            return citation
    except Exception as e:
        print(e)
        return None

async def get_intext(doi):
    authors = await get_authors(doi)
    citation = await get_cite(doi)
    year = citation[citation.index("(")+1:citation.index(").")]
    
    num_authors = len(authors)

    in_text = "("
    
    if num_authors == 1:
        in_text += authors[0]['family']
    elif num_authors == 2:
        in_text += f"{authors[0]['family']} and {authors[1]['family']}"
    elif num_authors == 3:
        in_text += f"{authors[0]['family']}, {authors[1]['family']} and {authors[2]['family']}"
    elif num_authors > 3:
        in_text += f"{authors[0]['family']} et al."
    
    in_text += f", {year})"
    return in_text
