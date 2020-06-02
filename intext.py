import requests



#curl -LH "Accept: application/rdf+xml;q=0.5, application/vnd.citationstyles.csl+json;q=1.0" https://doi.org/10.1126/science.169.3946.635


doi = "https://doi.org/10.1108/MAJ-09-2018-2004"


headers = {"Accept": "application/rdf+xml;q=0.5, application/vnd.citationstyles.csl+json;q=1.0"}


r = requests.post(doi, headers=headers).json()
#print(r)
authors = r["author"]

print(authors)
InText = ""



citation = "Haapamäki, E., & Sihvonen, J. (2019). Cybersecurity in accounting research. Managerial Auditing Journal, 34(7), 808–834. Available from: https://doi.org/10.1108/maj-09-2018-2004 [Accessed: 2 June 2020]."


published_date = citation[citation.index("(")+1:citation.index(").")]


if len(authors) > 3:
    InText = authors[0]["family"] + " et al.," + published_date
    print(InText)

elif len(authors) == 3:
    InText = f"({authors["family"][0].title()},  {authors["family"][1].title()} and {authors["family"][2].title()}, {published_date})"
    print(InText)

elif len(authors) == 2:
    InText = f"({authors["family"][0].title()} and {authors["family"][1].title()}, {published_date})"
    print(InText)

elif len(authors) == 1:
    InText = f"({authors["family"][0].title()}, {published_date})"
    print(InText)


