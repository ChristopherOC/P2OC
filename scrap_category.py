"""Programme ayant pour but de récolter toute les infomations
d'une catégorie en faisant appel au programme scrap_category
à travers plusieurs pages"""
import requests
from bs4 import BeautifulSoup
import argparse
import csv
from scrap_book import scrap_book
import os.path

"""Création d'une fonction scrap_category passant le paramètre
url afin de trouver chaque article de la catégorie"""


def scrap_category(url):

    """L'existence de l'url est véirfiée"""

    request_category = requests.get(url)

    if request_category.ok:

        book_data_list = []
        home_soup = BeautifulSoup(request_category.text, 'html.parser')
        books_url = [el['href'].replace("../../..",
                                        "https://books.toscrape.com/catalogue")
                     for el in home_soup.select('article h3 a')]

        button = home_soup.select_one("#default > div > div > div > div > section > div:nth-child(2) >\
                    div > ul > li.next > a")

        while True:

            """Tant que le bouton pour accéder à une page suivante
            de la catégorie est disponible, le programme
            s'exécute à travers chacune d'entre elle en modifiant l'url"""

            if button is not None:
                href = url.replace('index.html', button['href'])
                request_page = requests.get(href)
                page_soup = BeautifulSoup(request_page.text, 'html.parser')
                new_list_book = [el['href'].replace(
                    "../../..", "https://books.toscrape.com/catalogue")
                    for el in page_soup.select('article h3 a')]
                for new_book in new_list_book:
                    books_url.append(new_book)
                button = page_soup.select_one(
                    "#default > div > div > div > div > section > \
                     div:nth-child(2) > div > ul > li.next > a")
            else:
                break

        for product_page_url in books_url:

            """Pour chaque livre trouvé dans une page de la catégorie,
            le programme scrap_book est appelé pour récupérer les
            inforamtions demandées"""

            book_data = scrap_book(product_page_url)
            book_data_list.append(book_data)

            """Création d'un fichier local afin de stocker les 
            informations récoltées par l'exécution du programme """

            current_directory = os.getcwd()
            category_directory = os.path.join(current_directory,
                                              book_data['category'])
            if not os.path.exists(category_directory):
                os.makedirs(category_directory)

            image_directory = os.path.join(category_directory, 'image')
            if not os.path.exists(image_directory):
                os.makedirs(image_directory)

            """Récupération des images de chaque livre pour les ajouter à un
            dossier local"""

            img_data = requests.get(book_data['image_url']
                                    ).content  # Enregistre les url
            # des img dans un dossier

            with open(book_data['category'] + '/image/'
                      + book_data['universal_product_code'] + '.jpg', "wb")\
                    as dossier_img:
                dossier_img.write(img_data)

        """Création d'un fichier CSV ou sont retranscrites
        les données de façon ordonnée"""

        with open('category.csv', 'w', newline='', encoding="utf-8") as \
                csv_file:
            fieldnames = book_data_list[0].keys()
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames,
                                    delimiter=';')
            writer.writeheader()
            for book in book_data_list:
                writer.writerow(book)

        print("Scrap de la catégorie avec succès")


"""Création d'une fonction main pour exécuter le programme
en y ajoutant un argument url"""


def main():
    parser = argparse.ArgumentParser(
        description="saisir l'url pour scraper la catégorie")
    parser.add_argument('url', type=str, help='lien de la catégorie')
    args = parser.parse_args()
    scrap_category(args.url)


if __name__ == '__main__':
    main()
