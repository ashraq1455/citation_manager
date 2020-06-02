import asyncio
import aiohttp

a_headers = {"Accept": "application/rdf+xml;q=0.5, application/vnd.citationstyles.csl+json;q=1.0"}
c_headers = {"Accept": "text/x-bibliography", "style": "harward"}

#doi = "10.1108/MAJ-09-2018-2004" 2
#doi = "10.1108/MAJ-01-2018-1766" 3
#doi = "10.1108/MAJ-03-2018-1831" 3
#doi = "10.1108/MAJ-10-2017-1673" 4
doi = "10.1108/MAJ-08-2014-1065"

async def get_authors(doi):
    async with aiohttp.ClientSession() as session:
        link = f"https://doi.org/{doi}"
        async with session.get(link, headers=a_headers) as res:
            response = await res.json()
    authors = response['author']
    return authors

async def get_date(doi):
    async with aiohttp.ClientSession() as session:
        link = f"https://doi.org/{doi}"
        async with session.get(link, headers=c_headers) as res:
            citation = await res.text()
        date = citation[citation.index("(")+1:citation.index(").")]
        return date


async def make_intext(doi):
    authors = await get_authors(doi)
    num_authors = len(authors)
    auth_text = "("
    if num_authors == 1:
        auth_text = authors[0]['family']
    elif num_authors == 2:
        auth_text += f"{authors[0]['family']} & {authors[1]['family']}"
    elif num_authors == 3:
        auth_text += f"{authors[0]['family']}, {authors[1]['family']} & {authors[2]['family']}"
    elif num_authors == 4:
        auth_text += f"{authors[0]['family']}, {authors[1]['family']}, {authors[2]['family']} & {authors[3]['family']}"
    elif num_authors > 4:
        auth_text += f"{authors[0]['family']} et al."

    year = await get_date(doi)
    auth_text += f", {year})"
    print(auth_text)


loop = asyncio.get_event_loop()
loop.run_until_complete(make_intext(doi))
