from bs4 import BeautifulSoup
import requests
from urllib.request import urlopen
import models
import stores
import json
import time
from selenium import webdriver
from routes import anhoch
from product_types import get_type
from selenium.common.exceptions import *
from selenium.webdriver.common.by import By


def anhoch_scrape():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.19582',
    }
    DRIVER_PATH = 'chromedriver'
    driver = webdriver.Chrome(executable_path=DRIVER_PATH)

    for key, url in anhoch.items():
        print(f"{key}: {url}")
        products = []
        i = 1

        while True:
            # page = requests.get(f"{url}{i}/", headers=headers)
            # soup = BeautifulSoup(page.content, 'html.parser')
            driver.get(url)

            product_tags = driver.find_elements(
                By.XPATH, '/html/body/div[3]/div/div/div/section/div/div[2]/section/div/div[2]/div/div/div[3]/ul/li')
            print(product_tags)
            # if len(product_tags) == 0:
            #     break

            for product in product_tags:
                product_object = models.Product(
                    store_name=stores.__ANHOCH__, product_type=get_type(key))
                print('product object created')

                product_details_url = product.find_element(
                    By.XPATH, './/*[@class="pbox thumbnail "]/div[1]/a')

                name = product_details_url.text.strip()
                print("Name: " + name)
                product_object.name = name

                product_url = product_details_url.get_attribute('href').strip()
                print("Url: " + product_url)
                product_object.product_url = product_url

                original_id = product.get_attribute('data-id').strip()
                print("OGID: " + original_id)
                product_object.original_id = original_id


                # Open a new window
                driver.execute_script("window.open('');")

                # Switch to the new window and open URL B
                driver.switch_to.window(driver.window_handles[1])
                driver.get(product_url)

                # …Do something here
                print('details page')
                brand = "/"
                try:
                    driver.find_element(By.XPATH, '//*[@id="product"]/div[1]/div[2]/section/div/div[2]/div/div[2]/a').text.strip()
                except Exception:
                    print("brand not found setting /")
                print("Brand: " + brand)
                product_object.brand = brand

                # Close the tab with URL B
                driver.close()

                # Switch back to the first tab with URL A
                driver.switch_to.window(driver.window_handles[0])

                return

                details_page = requests.get(product_details_url)
                
                product_soup = BeautifulSoup(
                    details_page.content, 'html.parser')
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

# todo: add click next page
            i += 1
            print("Sleeping 2.5 seconds after changing category page")
            time.sleep(2.5)

        with open(f"scraped_data/anhoch_{key}.json", "w", encoding="utf-8") as f:
            json.dump(products, f, ensure_ascii=False, indent=4)

    driver.quit()
