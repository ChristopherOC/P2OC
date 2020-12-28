import requests
from bs4 import BeautifulSoup

def bookOne():
    url = input("Saisissez l'url du livre à scrapper : ")  # URL à scraper
    print("L'url :", url)  # Affiche l'Url produit
    r = requests.get(url)  # Cherche l'Url en question
    if r.ok:  # Si l'url existe
        r.encoding = 'utf8'
        soup = BeautifulSoup(r.text, 'lxml')
        titre = soup.find('h1')  # Trouve le titre
        print("Le titre est : ", titre.text)
    x = soup.findAll('tr') #Cherche les valeurs du tableau
    for tr in x:
        title = tr.find('th')
        price = tr.find('td')

        print(title.text, " : ", price.text.replace('Â', ''))

    image = soup.select("#product_gallery > div > div > div > img")[0]['src'][5:] # Cherche l'Url de l'image
    print("L'url de l'image :", 'http://books.toscrape.com' + image)

    cat = soup.select("#default > div > div > ul > li:nth-child(3) > a")[0].text # Cherche la catégorie du livre
    print("La catégorie est : ", cat)

    description = soup.find(id='product_description').findNext('p').text# Cherche la description
    print("La description produit : ", description)

    rating = soup.find('p', {"class": "star-rating"})['class'][1] # Cherche la note du livre
    note = ['Zero', 'One', 'Two', 'Three', 'Four', 'Five']
    print("Product Rating : ", note.index(rating))

bookOne()