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
            page = requests.get(f"{url}{i}/", headers=headers)
            soup = BeautifulSoup(page.content, 'html.parser')

            product_tags = soup.select('li.span3.product-fix')
            print("len is ", len(product_tags))
            if len(product_tags) == 0:
                break

            for product in product_tags:
                product_details_url = product.select_one(
                    'div.product-name > a')['href']
                print("Url: " + product_details_url)
                # if product_details_url != 'https://anhoch.com/product/599873143/atx-mid-tower-case-thermaltake-j21-tempered-glass':
                #     continue
                details_page = requests.get(product_details_url)
                print('details page')
                product_soup = BeautifulSoup(
                    details_page.content, 'html.parser')

                product_object = models.Product(
                    store_name=stores.__ANHOCH__, product_url=product_details_url, product_type=get_type(key))
                print('product object created')
                product_object.name = product_soup.select_one(
                    'div.box-heading > h3').text.strip()
                print("Name: " + product_object.name)
                # tags = product_soup.select('div.product-desc')
                product_object.original_id = product['data-id'].strip()
                print("OGID: " + product_object.original_id)
                # product_object.brand = product.select_one('div.product-price.clearfix > div:second-child > strong').text.strip()
                if (len(product_soup.select('div.product-desc > a')) > 0):
                    product_object.brand = product_soup.select(
                        'div.product-desc > a')[0].get_text(strip=True)
                else:
                    product_object.brand = ""
                print("Brand: " + product_object.brand)
                product_image_tags = product_soup.select(
                    'div#product_gallery > img')
                for image in product_image_tags:
                    product_object.image_url += image['src'].strip() + ";"
                print("ImgURL: " + product_object.image_url)
                product_object.description = product_soup.select_one(
                    'div.span8.clearfix').text
                print("Description: " + product_object.description)
                product_object.price_mkd = product_soup.select_one(
                    'div.price > span.nm').text
                print("Price: " + product_object.price_mkd)

                store_tags = product_soup.select(
                    'div.span4.clearfix.pad5 > ul > li')
                for store_tag in store_tags:
                    if "icon-ok" in store_tag.select_one('i')['class']:
                        product_object.availability_array += f"{store_tag.select_one('span.padl5 > a > b').text.strip()};"
                print("Stores: " + str(product_object.availability_array))

                if product_object.availability_array != "":
                    product_object.is_available = True
                print("Availability: " + str(product_object.is_available))

                products.append(product_object.toJson())

                print(
                    f"Sleeping 20 second after adding new product #{len(products)}")
                time.sleep(20)

            i += 1
            print("Sleeping 2.5 seconds after changing category page")
            time.sleep(2.5)

        with open(f"scraped_data/anhoch_{key}.json", "w", encoding="utf-8") as f:
            json.dump(products, f, ensure_ascii=False, indent=4)
