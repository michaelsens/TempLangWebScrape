import requests
from bs4 import BeautifulSoup

def generate_url(language_group):
    urlStart = 'https://www.ethnologue.com/subgroups/'
    return urlStart + language_group

def scrape_page(language_group):
    url = generate_url(language_group)
    result = requests.get(url)
    src = result.content
    soup = BeautifulSoup(src, 'lxml')
    groups = soup.find("div", {"class": "view-content indent1"})
    recursive_search(groups.find("ul"))

def recursive_search(ul):
    if ul == None:
        return
    list = ul.find_all("li", recursive = False)
    for lang in list:
        print(lang.find('a').string)
        recursive_search(lang.find("ul"))

scrape_page("afro-asiatic")