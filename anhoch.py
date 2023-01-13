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
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def anhoch_scrape():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.19582',
    }
    DRIVER_PATH = 'driver'
    # driver = webdriver.Chrome(executable_path=DRIVER_PATH)
    driver = webdriver.Edge(executable_path=DRIVER_PATH)
    wait = WebDriverWait(driver, 15)

    for key, url in anhoch.items():
        print(f"{key}: {url}")
        products = []
        i = 1

        driver.get(url)
        while True:
            if i > 1:
                try:
                    driver.find_element(By.CLASS_NAME, 'icon-angle-right').click()
                except Exception:
                    print("End of pages")
                    break

            # wait untill se vcituva is over
            wait.until(EC.presence_of_element_located(
                (By.XPATH, '/html/body/div[3]/div/div/div/section/div/div[2]/section/div/div[2]/div/div/div[3]/ul/li')))

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

                wait.until(EC.presence_of_element_located(
                    (By.XPATH, '//*[@id="product"]/div[1]/div[2]/section/div/div[2]/div/div[2]/a')))
                brand = "/"
                try:
                    brand = driver.find_element(
                        By.XPATH, '//*[@id="product"]/div[1]/div[2]/section/div/div[2]/div/div[2]/a').text.strip()
                except Exception:
                    print("brand not found setting /")
                print("Brand: " + brand)
                product_object.brand = brand

                image_tags = driver.find_elements(
                    By.XPATH, '//*[@id="product_gallery"]/img')
                for image_tag in image_tags:
                    product_object.image_url += image_tag.get_attribute(
                        'src').strip() + ";"
                print("Images: " + product_object.image_url)

                description = driver.find_element(
                    By.XPATH, '//*[@id="description"]/div[1]/pre').text.strip()
                print("Description: " + description)
                product_object.description = description

                price = driver.find_element(
                    By.XPATH, '//*[@id="product"]/div[1]/div[2]/section/div/div[2]/div/div[1]/div/span[1]').text.strip()
                price = ''.join(char for char in price if char.isdigit())
                print("Price: " + price)
                product_object.price_mkd = price

                store_tags = driver.find_elements(By.XPATH, '//*[@id="description"]/div[2]/ul/li')
                for store_tag in store_tags:
                    icon_tag = store_tag.find_element(By.TAG_NAME, 'i')
                    if "icon-ok" in icon_tag.get_attribute('class'):
                        product_object.availability_array += store_tag.find_element(By.TAG_NAME, 'b').text.strip()
                print("Stores: " + str(product_object.availability_array))

                if product_object.availability_array != "":
                    product_object.is_available = True
                print("Availability: " + str(product_object.is_available))

                products.append(product_object.toJson())

                # Close the tab with URL B
                driver.close()

                # Switch back to the first tab with URL A
                driver.switch_to.window(driver.window_handles[0])

            i += 1

        with open(f"scraped_data/anhoch_{key}.json", "w", encoding="utf-8") as f:
            json.dump(products, f, ensure_ascii=False, indent=4)

    driver.quit()
