import json


class Product:
    def __init__(self, store_name, product_type):
        self.name = ""
        self.price_mkd = 0
        self.original_id = ""
        self.image_url = ""
        self.description = ""
        self.brand = ""
        self.is_available = False
        self.availability_array = ""
        self.product_url = ""
        self.store_name = store_name
        self.product_type = product_type

    def toJson(self):
        return {
            "name": self.name,
            "price_mkd": self.price_mkd,
            "original_id": self.original_id,
            "image_url": self.image_url,
            "description": self.description,
            "brand": self.brand,
            "is_available": self.is_available,
            "availability_array": self.availability_array,
            "product_url": self.product_url,
            "store_name": self.store_name,
            "product_type": self.product_type
        }
