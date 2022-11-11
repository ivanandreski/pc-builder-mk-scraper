from bs4 import BeautifulSoup
import requests
from urllib.request import urlopen
import models
import stores
import json
import time
from routes import anhoch
from product_types import get_type

def anhoch_scrape():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.19582',
    }
    
    for key, url in anhoch.items():
        print(f"{key}: {url}")
        products = []
        i = 1

        while True:
            page = requests.get(f"{url}{i}", headers=headers)
            soup = BeautifulSoup(page.content, 'html.parser')

            product_tags = soup.select('li.span3.span-first-child.product-fix')
            print("len is ", len(product_tags))
            if len(product_tags) == 0: 
                break

            for product in product_tags:
                product_details_url = product.select_one('div.product-name > a')['href']
                print("Url: " + product_details_url)
                details_page = requests.get(product_details_url)
                product_soup = BeautifulSoup(details_page.content, 'html.parser')

                product_object = models.Product(store_name=stores.__ANHOCH__, product_url=product_details_url, product_type=get_type(key))
                print(type(product_object.name))
                product_object.name = product_soup.select_one('div.box-heading > h3').text.strip()
                print("Name: " + product_object.name)
                tags = product_soup.select('div.product-desc')
                # product_object.original_id = product_soup.select_one('div.product-info-sku > span').text.split('КОД:')[1].strip()
                # print("OGID: " + product_object.original_id)
                # product_object.brand = product_soup.select_one('div.featured-attributes-rows > div:first-child > label').text.split('Бренд :')[1].strip()
                # print("Brand: " + product_object.brand)
                # product_object.is_available = product.select_one('div.product-info-stock-label > span.listing-info-row > img')['src']
                # print("Availability: " + product_object.is_available)
                product_image_tags = product.select('div.product_gallery > img')
                for image in product_image_tags:
                    product_object.image_url += image['src'].strip() + ";"
                print("ImgURL: " + product_object.image_url)
                product_object.description = product_soup.select_one('div.span8 clearfix').text
                print("Description: " + product_object.description)
                product_object.price_mkd = product_soup.select_one('div.price > span.nm').text
                print("Price: " + product_object.price_mkd)

                # todo: implement availability per stores
                
                products.append(product_object.toJson())
                
                print(f"Sleeping 2.5 second after adding new product #{len(products)}")
                # time.sleep(2.5)

            i += 1
            print("Sleeping 2.5 seconds after changing category page")
            # time.sleep(2.5)

        with open(f"scraped_data/anhoch_{key}.json", "w", encoding="utf-8") as f:
            json.dump(products, f, ensure_ascii=False, indent=4)
