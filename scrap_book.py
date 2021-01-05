import pip
import requests
from bs4 import BeautifulSoup
import argparse


def scrap_book():
    book_data = {}
    parser = argparse.ArgumentParser(description="saisir l'url pour scraper un livre")
    parser.add_argument('url', type=str, help='lien du livre')
    args = parser.parse_args()

    request_url = requests.get(args.url)  # Cherche l'Url en question
    if request_url.ok:  # Si l'url existe
        request_url.encoding = 'utf8'
        soup = BeautifulSoup(request_url.text, 'html.parser')
        book_data['titre'] = soup.find('h1').text  # Trouve le titre

    book_data['url'] = args.url
    book_data['universal_product_code'] = soup.select_one("#content_inner>article>table>tr:nth-child(1)>td").text
    book_data['price_excluding_taxe'] = soup.select_one("#content_inner > article > table > tr:nth-child(3) > td").text
    book_data['prince_including_taxe'] = soup.select_one("#content_inner > article > table > tr:nth-child(4) > td").text
    book_data['number_available'] = soup.select_one("#content_inner > article > table > tr:nth-child(6) > td").text
    book_data['image_url'] = soup.select_one("#product_gallery > div > div > div > img")['src'][5:]  # Url de l'image
    book_data['category'] = soup.select_one("#default > div > div > ul > li:nth-child(3) > a").text
    book_data['product_description'] = soup.select_one('#content_inner > article > p').text
    note = \
    soup.select_one('#content_inner > article > div.row > div.col-sm-6.product_main > p.star-rating.Three')['class'][1]
    book_data['review_rating'] = ['Zero', 'One', 'Two', 'Three', 'Four', 'Five'].index(note)
    return book_data


print(scrap_book())
