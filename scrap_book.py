""" Programme ayant pour but de collecter
différentes informations d'un livre à partir d'une url"""
import requests
from bs4 import BeautifulSoup
import argparse

"""Création d'une fonction main pour exécuter le programme scrap_book"""


def main():
    parser = argparse.ArgumentParser(
        description="saisir l'url pour scraper un livre")
    parser.add_argument('url', type=str, help='lien du livre')
    args = parser.parse_args()
    print(scrap_book(args.url))


"""Création de la fonction scrap_book passant le paramètre url
qui sera chargé de récupérer toute les informations
nécessaires pour un livre"""


def scrap_book(url):

    """Création d'une liste pour le livre ou chaque information
    récupérée à partir de celui-ci lui sera ajouté"""

    book_data = {}

    request_url = requests.get(url)  # Vérifie l'existence de l'url
    if request_url.ok:  # Si l'url existe
        request_url.encoding = 'utf8'
        soup = BeautifulSoup(request_url.text, 'html.parser')
        book_data['titre'] = soup.find('h1').text  # Trouve le titre
        book_data['url'] = url  # Trouve l'url
        book_data['universal_product_code'] = soup.select_one(
            "#content_inner>article>table>tr:nth-child(1)>td").text
        # Trouve l'UPC
        book_data['price_excluding_taxe'] = soup.select_one(
            "#content_inner > article > table > tr:nth-child(3) > td").text
        # Trouve le prix sans taxe
        book_data['prince_including_taxe'] = soup.select_one(
            "#content_inner > article > table > tr:nth-child(4) > td").text
        # Trouve le prix avec taxe
        book_data['number_available'] = soup.select_one(
            "#content_inner > article > table > tr:nth-child(6) > td").text
        # Trouve le nombre disponible d'article
        book_data['image_url'] = soup.select_one(".carousel img")['src'] \
            .replace("../../", "https://books.toscrape.com/")
        # Trouve l'url de l'image et la reconstitue
        book_data['category'] = soup.select_one(
            "#default > div > div > ul > li:nth-child(3) > a").text
        # Trouve la catégorie à laquelle appartient le livre
        description = soup.select_one('#content_inner > article > p')
        # Trouve la description du produit

        if description is not None:

            """Si la descritpion existe alors elle est retranscrite,
            le cas contraire un message est retourné"""

            book_data['product_description'] = description.text
        else:
            book_data['product_description'] = "Aucune description disponible"
        note = \
            soup.select_one('#content_inner > \
            article > div.row > div.col-sm-6.product_main > \
             p.star-rating')['class'][1]
        book_data['review_rating'] = ['Zero', 'One', 'Two',
                                      'Three', 'Four', 'Five'].index(note)
        # Trouve la note du livre en la comparant à une liste
        print(book_data)
        return book_data


if __name__ == '__main__':
    main()
