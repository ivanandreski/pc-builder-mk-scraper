from bs4 import BeautifulSoup
import requests
from urllib.request import urlopen
import base64
from urllib.request import urlopen
from urllib.error import HTTPError
import models
import routes
import stores
import product_types
import json

url = routes.setec['processors']

products = []

i = 1
while True:
    if i > 1: break

    page = requests.get(f"{url}{i}")
    soup = BeautifulSoup(page.content, 'html.parser')

    products = soup.find_all('.product.clearfix.product-hover')
    if len(products) == 0: break

    for product in products:
        product_details_url = product.select_one('div.right > div.name > a')['href']
        details_page = requests.get(product_details_url)
        product_soup = BeautifulSoup(details_page.content, 'html.parser')

        product_object = models.Product(store_name=stores.__SETEC__, product_url=product_details_url, product_type=product_types.__CPU__)

        product_object.name = product_soup.select_one('#title-page').text.strip()
        product_object.original_id = product.select_one('div.shifra').text.split('Шифра:')[1].strip()
        product_object.image_url = product.select_one('div.image > a > img')['src'].strip()
        product_object.description = product_soup.select_one('#tab-description').text.strip()
        product_object.brand = product_soup.select_one('div.description > a').text.strip()

        price_tag = product_soup.select_one('div.price > #price-old-product')
        if price_tag == None:
            price_tag = product_soup.select_one('div.price > #price-old')
        product_object.price_mkd = ''.join(filter(str.isdigit, price_tag.text))

        availability_list = []
        for store_tag in product_soup.select('div.dropdown2-menu > div'):
            if store_tag.select_one('img')['src'] == 'image/yes.png':
                store_name = store_tag.select_one('a').text.strip()
                availability_list.append(store_name)

        if len(availability_list) > 0:
            product_object.is_available = True
        product_object.availability_list = json.dumps(availability_list, ensure_ascii=False)
        
        products.append(json.dumps(product_object.__dict__, ensure_ascii=False))

    i += 1

with open("setec_processors.json", "w") as f:
    json.dumps(products, f, ensure_ascii=False)

