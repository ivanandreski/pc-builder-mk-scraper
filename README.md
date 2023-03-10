# PC Components Scraper MK

### Description
This web scraper is used to scrape products from Macedonian computer stores:
1. Anhoch
2. Setec
3. DDStore

### Instructions
1. Create a python virtual environment
2. Activate the virtual environment
3. Run `pip install -r requirements.txt`
4. Depending on the store you want to scrape run the following command:
    1. `python app.py "store name"` without the quotes
    2. Available store names are: `anhoch`, `setec`, `ddstore`
5. After the scraper is done, the files are outputed to the scraped_data folder
6. The products are categorised into diffrent files and they start with the store name followed by the category
7. If a file from a category already exists, that category is skipped

### Scraped data format
The scraped data output file is in Json format. It contains an array of objects which represent a product
Attributes
1. `name` - [string] Name of product
2. `price_mkd` - [string] Price in MKD Denar of product
3. `original_id` - [string] Original Id from the website of the product
4. `image_url` - [string] String of image urls separated by ;
5. `description` - [string] Description of product
6. `brand` - [string] Brand/Manufacturer of product
7. `is_available` - [bool] True if product is available in any store, based on the number of stores in the next attribute
8. `availability_array` - [string] String of shop names separated by ;
9. `product_url` - [string] Url of the product
10. `store_name` - [string] Name of the current store
11. `product_type` - [string] Category of product

### Example scraped data
```csharp
    {
        "name": "CPU AMD Ryzen 3 1200 AF Quad-Core 3.1GHz AM4 (12nm) 10MB TRAY w/o Cooler",
        "price_mkd": "4990",
        "original_id": "599869531",
        "image_url": "https://d1a68gwbwfmqto.cloudfront.net/img/products/full/yd1200bbm4kaf_1.jpg;",
        "description": "Specifications\n# of CPU Cores: 4\n# of Threads: 4\nBase Clock Speed: 3.1GHz\nMax Turbo Core Speed: 3.4GHz\nTotal L1 Cache: 384KB\nTotal L2 Cache: 2MB\nTotal L3 Cache: 8MB\nUnlocked: Yes\nCMOS: 12nm\nPackage: AM4\nPCI Express Version: PCIe 3.0\nThermal Solution: N/A\nDefault TDP / TDP: 65W\nMax Temps: 95°C\n\nSystem Memory\nMax System Memory Speed: 2667MHz\nSystem Memory Type: DDR4\nMemory Channels: 2\n\nKey Features\nSupported Technologies\nThe “Zen” Core Architecture\nAMD SenseMI Technology\nAMD VR Ready Processors\nAVX2\nFMA3\nXFR (Extended Frequency Range)\n\nFoundation\nProduct Family: AMD Ryzen™\nProduct Line: AMD Ryzen™ 3\nPlatform: Desktop\n\nMore Info:\nПовеќе за производот...",
        "brand": "AMD",
        "is_available": true,
        "availability_array": "Магацин - Анхоч Дирекција;",
        "product_url": "https://anhoch.com/product/599869531/cpu-amd-ryzen-3-1200-af-quad-core-31ghz-am4-12nm-10mb-tray-wo-cooler",
        "store_name": "Anhoch",
        "product_type": "CPU"
    },
```

### Technologies
1. Setec and DDStore scraper use BeautifulSoup4
2. Anhoch scraper uses Selenium
