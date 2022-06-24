import requests
from bs4 import BeautifulSoup
import re

def generate_url(language_group):
    urlStart = 'https://www.ethnologue.com/subgroups/'
    return urlStart + language_group

def scrape_page(language_group):
    url = generate_url(language_group)
    result = requests.get(url)
    src = result.content
    soup = BeautifulSoup(src, 'lxml')
    groups = soup.find("div", {"class": "view-content indent1"})
    recursive_search(groups.find("div", {"class": "item-list"}))

def recursive_search(item_list):
    if item_list == None:
        return
    list = item_list.find("ul").find_all("li", recursive = False)
    for lang in list:
        leaf = lang.find("div", class_= re.compile("^view view-language"), recursive = False)
        leaf_ul = leaf.select('div > div > div > ul')
        if leaf_ul != []: 
            leaf_list = leaf_ul[0].find_all("li", recursive = False)
            for leaf_lang in leaf_list:
                print(leaf_lang.find("span", {"class": "field-content"}).text)
        print(lang.find('a').string)
        recursive_search(lang.find("div", {"class": "item-list"}, recursive = False))

scrape_page("afro-asiatic")