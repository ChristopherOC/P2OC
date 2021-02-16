import pip
import requests
from bs4 import BeautifulSoup
import argparse


def main():
    parser = argparse.ArgumentParser(description="saisir l'url pour scraper un livre")
    parser.add_argument('url', type=str, help='lien du livre')
    args = parser.parse_args()
    print(scrap_book(args.url))



def scrap_book(url):
    book_data = {}

    request_url = requests.get(url)  # Cherche l'Url en question
    if request_url.ok:  # Si l'url existe
        request_url.encoding = 'utf8'
        soup = BeautifulSoup(request_url.text, 'html.parser')
        book_data['titre'] = soup.find('h1').text  # Trouve le titre

        book_data['url'] = url
        book_data['universal_product_code'] = soup.select_one("#content_inner>article>table>tr:nth-child(1)>td").text
        book_data['price_excluding_taxe'] = soup.select_one("#content_inner > article > table > tr:nth-child(3) > td").text
        book_data['prince_including_taxe'] = soup.select_one("#content_inner > article > table > tr:nth-child(4) > td").text
        book_data['number_available'] = soup.select_one("#content_inner > article > table > tr:nth-child(6) > td").text
        book_data['image_url'] = soup.select_one(".carousel img")['src'].replace("../../","https://books.toscrape.com/")  # Url de l'image
        book_data['category'] = soup.select_one("#default > div > div > ul > li:nth-child(3) > a").text
        description = soup.select_one('#content_inner > article > p')
        if description is not None:
            book_data['product_description'] = description.text
        else:
            book_data['product_description']= "Aucune description disponible"
        note = \
            soup.select_one('#content_inner > article > div.row > div.col-sm-6.product_main > p.star-rating')['class'][1]
        book_data['review_rating'] = ['Zero', 'One', 'Two', 'Three', 'Four', 'Five'].index(note)
        print(book_data)
        return book_data


if __name__ == '__main__':
    main()
