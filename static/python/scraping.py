from os.path import join
import requests
import json
import random
import time
from static.python.configs import *
from static.python.mongo_db import Mongo


mongo = Mongo()
site_ids = []


def get_response(url, payload):
    r = requests.post(url, verify=False, json=payload)
    response_dict = json.loads(r.text)
    time.sleep(random.randint(1, 6))

    return response_dict


def parse_site_ids(category_name, page_number):
    url = f"https://zwebapi.zapmarket.co.il/api/models/search/{page_number}/50/popularity/true"

    payload = {"aisles": category_name,
               "position": [{"lat": "32.0879585",
                             "lng": "34.7622266",
                             "addressName": "תל אביב",
                             "radius": 6}]}

    site_ids_dict = get_response(url=url,
                                 payload=payload)

    for site_id_dict in site_ids_dict["data"]:
        parsed_site_id_dict = {"site_id": site_id_dict["modelId"],
                               "category_name": category_name}

        site_ids.append(parsed_site_id_dict)


def get_site_ids():
    for category_name in categories.keys():
        for page_number in range(1, 3):
            parse_site_ids(category_name=category_name,
                           page_number=page_number)


def parse_product(product_dict, region_id, category_name, site_id):
    stores_from_product_dict = product_dict.get('stores')
    collection_name = "products"

    stores = [{"store_name": store['name'], "price": store['price']} for store in stores_from_product_dict]

    parsed_product_dict = {
        "barcode": product_dict.get('barcode', ''),
        "product_name": product_dict.get('name'),
        "product_id": site_id,
        "category_id": categories[category_name]["category_id"],
        "category_name": categories[category_name]["translated_name"],
        "stores": stores,
        "region_id": region_id,
        "region_name": regions_payloads[region_id]["payload"]["position"][0]["addressName"],
        "product_img": product_dict.get('imgUrl', '')
    }

    mongo.insert_to_db(collection_name=collection_name,
                       query_dict=parsed_product_dict)


def get_parsed_products(site_id, category_name):
    product_prefix = 'https://zwebapi.zapmarket.co.il/api/models/getModelPage/'
    product_url = join(product_prefix, site_id)

    for region_id in regions_payloads.keys():
        payload = regions_payloads[region_id]["payload"]

        product_dict = get_response(url=product_url,
                                    payload=payload)

        parse_product(product_dict=product_dict,
                      region_id=region_id,
                      category_name=category_name,
                      site_id=site_id)


if __name__ == '__main__':

    get_site_ids()
    fixed_site_ids = []

    for item in site_ids:
        if item not in fixed_site_ids:
            fixed_site_ids.append(item)

    for site_id_dict in fixed_site_ids:
        site_id = site_id_dict["site_id"]
        category_name = site_id_dict["category_name"]

        get_parsed_products(site_id=site_id,
                            category_name=category_name)


