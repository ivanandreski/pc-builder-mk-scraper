from bs4 import BeautifulSoup
import requests
from urllib.request import urlopen
import os.path
from urllib.request import urlopen
from urllib.error import HTTPError
import models
import routes
import stores
import product_types
import json
import time
from routes import setec
from product_types import get_type
from datetime import datetime

def setec_scrape():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.19582',
    }
    
    for key, url in setec.items():
        if os.path.isfile(f"./scraped_data/setec_{key}.json"):
            continue

        products = []
        i = 1

        while True:
            page = requests.get(f"{url}{i}", headers=headers)
            soup = BeautifulSoup(page.content, 'html.parser')

            product_tags = soup.select('.product.clearfix.product-hover')
            if len(product_tags) == 0: break

            for product in product_tags:
                product_details_url = product.select_one('div.right > div.name > a')['href']
                details_page = requests.get(product_details_url)
                product_soup = BeautifulSoup(details_page.content, 'html.parser')

                product_object = models.Product(store_name=stores.__SETEC__, product_url=product_details_url, product_type=get_type(key))

                product_object.name = product_soup.select_one('#title-page').text.strip()
                product_object.original_id = product.select_one('div.shifra').text.split('Шифра:')[1].strip()
                product_object.image_url = product.select_one('div.image > a > img')['src'].strip()
                product_object.description = product_soup.select_one('#tab-description').text.strip()
                product_object.brand = product_soup.select_one('div.description > a').text.strip()

                price_tag = product_soup.select_one('div.price > #price-old-product')
                if price_tag == None:
                    price_tag = product_soup.select_one('div.price > #price-old')
                product_object.price_mkd = ''.join(filter(str.isdigit, price_tag.text))

                availability_list = ""
                for store_tag in product_soup.select('div.dropdown2-menu > div'):
                    if store_tag.select_one('img')['src'] == 'image/yes.png':
                        store_name = store_tag.select_one('a').text.strip()
                        availability_list += f"{store_name};"

                if availability_list != "":
                    product_object.is_available = True
                product_object.availability_array = availability_list
                
                products.append(product_object.toJson())
                
                print(f"Sleeping 10 second after adding new product #{len(products)}")
                time.sleep(10)

            i += 1
            print("Sleeping 2.4 seconds after changing category page")
            time.sleep(2.4)

        today = datetime.today().strftime('%d-%m-%Y')
        with open(f"scraped_data/setec_{today}/setec_{key}.json", "w", encoding="utf-8") as f:
            json.dump(products, f, ensure_ascii=False, indent=4)
