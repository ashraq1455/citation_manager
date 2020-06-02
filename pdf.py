import requests
from bs4 import BeautifulSoup as soup

URL = "https://scihub.wikicn.top/https://doi.org/10.1016/j.giq.2017.02.007"
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

req = requests.get(URL, headers=headers)

html = soup(req.content.decode("utf-8"), "html.parser")

pdf_link = html.find("iframe", {"id": "pdf"})

print(pdf_link["src"])
