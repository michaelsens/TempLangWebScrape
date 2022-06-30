# Last update date: 2022-06-28
# Original Author: Michael Sensale
# Last update by: Michael Sensale
import requests
from bs4 import BeautifulSoup
import re

# Last update date: 2022-06-25
# @description Generates an ethnologue url for a given language group
# @author Michael Sensale
# @param {String} language_group
# @returns complete language group url
def generate_url(language_group):
    urlStart = 'https://www.ethnologue.com/subgroups/'
    return urlStart + language_group

# Last update date: 2022-06-25
# @description Scrapes the language tree of a specific language group from the 
# ethnolougue website, currently prints information to terminal
# @author Michael Sensale
# @param {String} language_group
# @returns #TODO: Return formatted data
def scrape_page(language_group):
    url = generate_url(language_group) 
    result = requests.get(url)
    src = result.content
    soup = BeautifulSoup(src, 'lxml')
    groups = soup.find("div", {"class": "view-content indent1"})
    recursive_search(groups.find("div", {"class": "item-list"}), "") #begin recursive search on the top level language list

# Last update date: 2022-06-25
# @description scrpae_page recursive helper method, recursivly searches through all the language data in the higherachy
# @author Michael Sensale
# @param {String} item_list, temp_indent
# @returns #TODO: Store and eturn data
def recursive_search(item_list, temp_indent):
    if item_list == None: return #base case: if there are no lower levels in the tree
    list = item_list.find("ul").find_all("li", recursive = False)
    for lang in list: #loop through the next level of languages, accessing their data and calling recursive search on them
        leaf = lang.find("div", class_= re.compile("^view view-language"), recursive = False)
        leaf_ul = leaf.select('div > div > div > ul')
        if leaf_ul != []: #if the language is the special base case, data needs to be accessed differently
            leaf_list = leaf_ul[0].find_all("li", recursive = False)
            for leaf_lang in leaf_list:
                print(temp_indent + leaf_lang.find("span", {"class": "field-content"}).text)
        print(temp_indent + lang.find('a').string)
        recursive_search(lang.find("div", {"class": "item-list"}, recursive = False), temp_indent + "    ")

scrape_page("afro-asiatic")