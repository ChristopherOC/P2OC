import requests
from bs4 import BeautifulSoup
from scrap_category import scrap_category


def scrap_site():
    resp = requests.get("https://books.toscrape.com/index.html")
    if resp.ok:
        site_soup = BeautifulSoup(resp.text, "html.parser")
        list_category = site_soup.find("ul", {"class": "nav"}).findNext('li').findNext('ul').findAll('li')
        for category in list_category:
            category_url = "https://books.toscrape.com/" + category.find('a')['href']
            scrap_category(category_url)


if __name__ == '__main__':
    scrap_site()


