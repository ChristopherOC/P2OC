import requests
from bs4 import BeautifulSoup

def category():
    url = input("Saisir l'url de la catégorie a scraper : ")
    home = requests.get(url)

    if home.ok:
        homeSoup = BeautifulSoup(home.text, 'lxml')
        books = homeSoup.findAll('article')
        for book in books:
            a = book.find('a')
            link = a['href']
            each = (link.replace('../../../', 'https://books.toscrape.com/catalogue/'))
            print(each)

            bookrequest = requests.get(each)  # Cherche l'Url en question
            if bookrequest.ok: # Si l'url existe
                bookSoup = BeautifulSoup(bookrequest.text, 'lxml')
                titre = bookSoup.find('h1')  # Affiche le titre
                print("Le titre est : ", titre.text)

                x = bookSoup.findAll('tr')
                for tr in x:
                    title = tr.find('th')
                    price = tr.find('td')

                    print(title.text, " : ", price.text.replace('Â', ''))

                image = bookSoup.select("#product_gallery > div > div > div > img")[0]['src'][5:] # Cherche l'url de l'image
                print("L'url de l'image :", 'http://books.toscrape.com' + image)

                cat = bookSoup.select("#default > div > div > ul > li:nth-child(3) > a")[0].text # Cherche la catégorie
                print("La catégorie est : ", cat)

                description = bookSoup.find(id='product_description').findNext('p').text # Cherche la description
                print("La description produit : ", description)

                rating = bookSoup.find('p', {"class": "star-rating"})['class'][1]  # Cherche la note du livre
                note = ['Zero', 'One', 'Two', 'Three', 'Four', 'Five']
                print("Product Rating : ", note.index(rating))
category()