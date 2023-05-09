from os.path import join
import sqlite3
import requests
import json


DATABASE = 'pingu.db'

url_suffixes = ['7333',
                '3396',
                '934515',
                '6701']

stores = ['ויקטורי דיזנגוף',
          'שופרסל שלי בן יהודה',
          'מגה דיזינגוף',
           'am:pm בן יהודה 30']


def get_product_dict(url):
    payload = {"position":[{"lat": "32.0879585",
                            "lng": "34.7622266",
                            "addressName": "תל אביב",
                            "radius": 6}],
               "cartId": "CartModels/ce30a1b3-ca0b-4499-8288-16cfbb1070b2"}

    r = requests.post(url, verify=False, json=payload)
    product_dict = json.loads(r.text)

    return product_dict


def parse_product(product_dict):
    barcode = product_dict.get('barcode', '')
    product_name = product_dict.get('name', '')
    product_img = product_dict.get('imgUrl', '')

    # insert to products table
    with sqlite3.connect(DATABASE) as connection:
        try:
            cursor = connection.cursor()
            q = "INSERT INTO products (product_id, product_name, product_image) VALUES (?, ?, ?)"
            cursor.execute(q, (barcode, product_name, product_img))
            connection.commit()
        except Exception as e:
            print(e)

    # insert product to stores table
    stores_from_product_dict = product_dict.get('stores')

    for store in stores_from_product_dict:
        store_name = store['name']

        if store_name in stores:
            product_price = store['price']

            with sqlite3.connect(DATABASE) as connection:
                try:
                    cursor = connection.cursor()
                    q = "INSERT INTO stores (store_name, product_id, product_price) VALUES (?, ?, ?)"
                    cursor.execute(q, (store_name, barcode, product_price))
                    connection.commit()
                except Exception as e:
                    print(e)


def update_products_values():
    product_prefix = 'https://zwebapi.zapmarket.co.il/api/models/getModelPage/'
    product_urls = [join(product_prefix, product_suffix) for product_suffix in url_suffixes]

    for product_url in product_urls:
        product_dict = get_product_dict(url=product_url)
        parse_product(product_dict=product_dict)


def execute_queries_from_file(file_path):
    queries_str = open(file_path, 'r').read()
    queries = queries_str.replace('\n', '').split(';')
    queries = [query.strip() for query in queries if query != '']

    for q in queries:
        with sqlite3.connect(DATABASE) as connection:
            try:
                cursor = connection.cursor()
                cursor.execute(q)

            except Exception as e:
                print(e)


def get_product_names():
    with sqlite3.connect(DATABASE) as connection:
        cursor = connection.cursor()
        products_list = []
        q = "SELECT product_name, product_id FROM products"

        try:
            rows = cursor.execute(q)
            products_list = [{'product_name': r[0], 'product_id': r[1]} for r in rows]

        except Exception as e:
            print(e)

        return products_list


def insert_to_cart(user_name, product_id, quantity):
    with sqlite3.connect(DATABASE) as connection:
        try:
            cursor = connection.cursor()
            q = "INSERT INTO cart (user_name, product_id, quantity) VALUES (?, ?, ?)"
            cursor.execute(q, (user_name, product_id, quantity))
            connection.commit()

        except Exception as e:
            print(e)


def show_cart(user_name):
    with sqlite3.connect(DATABASE) as connection:
        cursor = connection.cursor()
        cart_list = []
        q = "select a.product_name, sum(b.quantity) " \
            "from products a " \
            "join cart b " \
            "on a.product_id=b.product_id " \
            "and b.user_name='%s'" \
            "group by a.product_name" % user_name

        try:
            rows = cursor.execute(q)
            cart_list = [{'product_name': r[0], 'quantity': r[1]} for r in rows]

        except Exception as e:
            print(e)

        return cart_list


def remove_buyer_products(user_name):
    with sqlite3.connect(DATABASE) as connection:
        try:
            cursor = connection.cursor()
            q = "DELETE FROM cart WHERE user_name='%s'" % user_name
            cursor.execute(q)
            connection.commit()
        except Exception as e:
            print(e)


def get_three_best_offers(offers):
    best_offers = sorted(offers, key=lambda x: x['total_price'])

    if len(best_offers) >= 3:
        return best_offers[:3]

    else:
        return best_offers


def get_best_offers(user_name):
    with sqlite3.connect(DATABASE) as connection:
        cursor = connection.cursor()
        stores_list = []

        q = "select a.store_name, sum(a.product_price) " \
            "from stores a " \
            "join cart b " \
            "on a.product_id=b.product_id " \
            "and b.user_name='%s' " \
            "group by a.store_name" % user_name

        try:
            rows = cursor.execute(q)
            stores_list = [{'store_name': r[0], 'total_price': r[1]} for r in rows]

        except Exception as e:
            print(e)

        best_offers = get_three_best_offers(stores_list)

        return best_offers


def add_user(user_name: str, user_password: str):
    with sqlite3.connect(DATABASE) as connection:
        try:
            cursor = connection.cursor()
            q = "INSERT INTO users (user_name, user_password) VALUES (?, ?)"
            cursor.execute(q, (user_name, user_password))
            connection.commit()
        except Exception as e:
            print(e)


def check_auth_user(user_name, user_password):
    with sqlite3.connect(DATABASE) as connection:
        cursor = connection.cursor()
        q = "SELECT user_name from users where user_name='%s' and user_password='%s'" % (user_name, user_password)

        try:
            rows = cursor.execute(q)           
            rows_list = [row[0] for row in rows]
            
            if len(rows_list) > 0:
                return True, rows_list[0]

            else:
                return False, ''

        except Exception as e:
            print(e)


def get_users():
    """
    :return: a ste of users' names is returned
    """
    with sqlite3.connect(DATABASE) as connection:
        try:
            cursor = connection.cursor()
            q = "SELECT user_name FROM users"
            rows = cursor.execute(q)
            return set([r[0] for r in rows])
        except Exception as e:
            print(e)


