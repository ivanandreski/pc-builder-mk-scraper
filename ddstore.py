from bs4 import BeautifulSoup
import requests
from urllib.request import urlopen
import models
import stores
import json
import os.path
from routes import ddstore
from product_types import get_type

def ddstore_scrape():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.19582',
    }
    
    for key, url in ddstore.items():
        if os.path.isfile(f"./scraped_data/ddstore_{key}.json"):
            continue

        products = []
        i = 1

        while True:
            page = requests.get(f"{url}{i}", headers=headers)
            soup = BeautifulSoup(page.content, 'html.parser')

            product_tags = soup.select('li.item.product.product-item')
            print("len is ", len(product_tags))
            if len(product_tags) == 0: 
                break

            for product in product_tags:
                product_details_url = product.select_one('div.image-grid > a')['href']
                # if(product_details_url != "https://ddstore.mk/cpu-amd-athlon-pro-300ge-dual-core-3-4ghz-am4-5mb-tray-w-radeon-vega-3-graphics-w-o-cooler.html"):
                #     continue
                print("Url: " + product_details_url)
                details_page = requests.get(product_details_url)
                product_soup = BeautifulSoup(details_page.content, 'html.parser')

                product_object = models.Product(store_name=stores.__DDSTORE__, product_url=product_details_url, product_type=get_type(key))
                print(type(product_object.name))
                product_object.name = product_soup.select_one('h1.page-title > span.base').text.strip()
                print("Name: " + product_object.name)
                product_object.original_id = product_soup.select_one('div.product-info-sku > span').text.split('КОД:')[1].strip()
                print("OGID: " + product_object.original_id)
                product_object.image_url = product.select_one('img.product-image-photo')['src'].strip()
                print("ImgURL: " + product_object.image_url)
                description_tag = product_soup.select_one('div.product.attribute.description > div.value')
                if description_tag is not None:
                    product_object.description = description_tag.text.strip()
                    print("Description: " + product_object.description)
                additional_description = product_soup.select('label.for-tooltip')
                product_object.description = product_object.description + "\n"
                for ad in additional_description:
                    product_object.description = product_object.description + f"{ad.text}\n"
                print("Done add desc")
                product_object.brand = product_soup.select_one('div.featured-attributes-rows > div:first-child > label').text.split('Бренд :')[1].strip()
                print("Brand: " + product_object.brand)
                if product.select_one('span.price') is None:
                    continue
                product_object.price_mkd = ''.join(filter(str.isdigit, product.select_one('span.price').text))
                print("Price: " + product_object.price_mkd)

                product_object.availability_list = "DDStore LTD (ДДСтор);"

                availability_image_src = product.select_one('div.product-info-stock-label > span.listing-info-row > img')['src']
                print("Availability image src: " + availability_image_src)
                if 'not-available' in availability_image_src: product_object.is_available = False
                elif 'available' in availability_image_src: product_object.is_available = True
                else: product_object.is_available = None
                
                products.append(product_object.toJson())
                
                print(f"Sleeping 2.5 second after adding new product #{len(products)}")
                # time.sleep(2.5)

            i += 1
            print("Sleeping 2.5 seconds after changing category page")
            # time.sleep(2.5)

        with open(f"scraped_data/ddstore_{key}.json", "w", encoding="utf-8") as f:
            json.dump(products, f, ensure_ascii=False, indent=4)
