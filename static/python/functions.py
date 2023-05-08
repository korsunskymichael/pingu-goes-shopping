import sqlite3

DATABASE = 'pingu.db'
"""
url_suffixes = ['31433c9b-da59-46e5-9671-bcc680957af7']


    def __init__(self):
        self.product_prefix = 'https://zwebapi.zapmarket.co.il/api/models/getModelPage/'
        self.product_urls = [join(self.product_prefix, product_suffix) for product_suffix in url_suffixes]


    def get_product_dict(self, url):
        r = requests.post(url, verify=False)
        product_dict = json.loads(r.text)

        return product_dict

    def parse_product(self, product_configuration):
        product_dict = self.get_product_dict()

        product_configuration['id'] = product_dict.get('id')
        product_configuration['model_id'] = product_dict.get('', '')
        product_configuration['barcode'] = product_dict.get('barcode', '')
        product_configuration['name'] = product_dict.get('name', '')
        product_configuration['is_weighable'] = product_dict.get('isWeighable', '')
        product_configuration['min_price'] = product_dict.get('minPrice', '')
        product_configuration['max_price'] = product_dict.get('maxPrice', '')
        product_configuration['aisle_id'] = product_dict.get('aisleId', '')
        product_configuration['cat_id'] = product_dict.get('catId', '')
        product_configuration['sub_catId'] = product_dict.get('subCatId', '')
        product_configuration['product_quantity'] = product_dict.get('productQuantity', '')
        product_configuration['unit_quantity'] = product_dict.get('unitQuantity', '')
        product_configuration['min_price_per_unit'] = product_dict.get('minPricePerUnit', '')
        product_configuration['max_price_per_unit'] = product_dict.get('maxPricePerUnit', '')
        product_configuration['min_unit_of_measure_text'] = product_dict.get('minUnitOfmeasureText', '')
        product_configuration['min_unit_of_measure_amount'] = product_dict.get('minUnitOfmeasureAmount', '')

        product = Product(product_configuration=product_configuration)

        return product

"""
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


def insert_to_cart(buyer_id, product_id, quantity):
    with sqlite3.connect(DATABASE) as connection:
        try:
            cursor = connection.cursor()
            q = "INSERT INTO cart (buyer_id, product_id, quantity) VALUES (?, ?, ?)"
            cursor.execute(q, (buyer_id, product_id, quantity))
            connection.commit()

        except Exception as e:
            print(e)


def show_cart(buyer_id):
    with sqlite3.connect(DATABASE) as connection:
        cursor = connection.cursor()
        cart_list = []
        q = "select a.product_name, sum(b.quantity) " \
            "from products a " \
            "join cart b " \
            "on a.product_id=b.product_id " \
            "and b.buyer_id='%s'" \
            "group by a.product_name" % buyer_id

        try:
            rows = cursor.execute(q)
            cart_list = [{'product_name': r[0], 'quantity': r[1]} for r in rows]

        except Exception as e:
            print(e)

        return cart_list


def remove_buyer_products(buyer_id):
    with sqlite3.connect(DATABASE) as connection:
        try:
            cursor = connection.cursor()
            q = "DELETE FROM cart WHERE buyer_id='%s'" % buyer_id
            cursor.execute(q)
            connection.commit()
        except Exception as e:
            print(e)


def get_three_best_offers(offers):
    best_offers = sorted(offers, key=lambda x: x['total_price'])
    print(best_offers)

    if len(best_offers) >= 3:
        return best_offers[:3]

    else:
        return best_offers


def get_best_offers(buyer_id):
    with sqlite3.connect(DATABASE) as connection:
        cursor = connection.cursor()
        stores_list = []

        q = "select a.store_name, sum(a.product_price) " \
            "from stores a " \
            "join cart b " \
            "on a.product_id=b.product_id " \
            "and b.buyer_id='%s' " \
            "group by a.store_name" % buyer_id

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


def get_users():
    with sqlite3.connect(DATABASE) as connection:
        try:
            cursor = connection.cursor()
            q = "SELECT user_name FROM users"
            rows = cursor.execute(q)
            return set([r[0] for r in rows])
        except Exception as e:
            print(e)


def check_username(user_name: str, user_password: str):
    with sqlite3.connect(DATABASE) as connection:
        try:
            cursor = connection.cursor()
            q = "SELECT * FROM users WHERE user_name='%s' AND user_password='%s'" % (user_name, user_password)
            rows = cursor.execute(q)
            rowsList = [row for row in rows]
            return (len(rowsList) > 0)
        except Exception as e:
            print(e)

