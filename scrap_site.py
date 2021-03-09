"""Programme exécutant scrap_catrgory sur l'ensemble du site"""
import requests
from bs4 import BeautifulSoup
from scrap_category import scrap_category

"""création de la fonction scrap_site qui passe l'url du site
afin de récupérer toute les informations via la fonction
scrap_book et scrap_category"""


def scrap_site():
    resp = requests.get("https://books.toscrape.com/index.html")
    if resp.ok:

        """Si l'url est existante alors le programme peut continuer à 
        s'exécuter"""

        site_soup = BeautifulSoup(resp.text, "html.parser")
        list_category = site_soup.find("ul", {"class": "nav"}).findNext(
            'li').findNext('ul').findAll('li')

        for category in list_category:

            """Pour toute les catégories trouvées dans l'index,
            le programme scrap_category est appelé"""

            category_url = "https://books.toscrape.com/" + \
                           category.find('a')['href']
            scrap_category(category_url)


if __name__ == '__main__':
    scrap_site()
