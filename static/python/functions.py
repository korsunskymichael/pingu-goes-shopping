import smtplib
import math
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from static.python.mongo_db import Mongo
from static.python.secret import Secret
from static.python.configs import allowed_mail_suffixes

mongo = Mongo()
secret = Secret()


##################################################################################
# login and signup functions
##################################################################################
def add_user(user_name: str, user_password: str):
    try:
        encrypted_password = secret.encrypt_password(password=user_password)

        q = {"user_name": user_name,
             "password": encrypted_password
             }

        mongo.insert_to_db(collection_name="users",
                           query_dict=q)

    except Exception as e:
        print(e)


def check_if_user_exists(user_name):
    try:
        q = {"user_name": user_name}

        docs = mongo.select_from_db(collection_name="users",
                                    query_dict=q)

        return len([r["user_name"] for r in docs]) > 0

    except Exception as e:
        print(e)


def check_auth_user(user_name, user_password):
    try:
        if " or " not in user_name.lower() and " and " not in user_name.lower() \
                and "=" not in user_name and ((user_name.endswith(allowed_mail_suffixes[0]) is True)
                                              or (user_name.endswith(allowed_mail_suffixes[0]) is True)):
            password = get_user_password(user_name=user_name)

            if password == user_password:
                return True, user_name

        else:
            return False, ''

    except Exception as e:
        print(e)


def get_user_password(user_name):
    try:
        q = {"user_name": user_name}

        docs = mongo.select_from_db(collection_name="users",
                                    query_dict=q)

        docs_list = [secret.decrypt_password(encrypted_password=r["password"]) for r in docs]

        if len(docs_list) > 0:
            return docs_list[0]

        else:
            return ''

    except Exception as e:
        print(e)


def send_password_recovery(user_name, password):
    sender_email = 'pingugoesshopping@gmail.com'
    sender_password = 'ibtlmqsvqojybqvn'

    smtp_server = "smtp.gmail.com"
    smtp_port = 587

    msg = MIMEMultipart()
    msg['Subject'] = "Hey! we found your password "
    msg.attach(MIMEText(f"password: {password}"))

    mail = smtplib.SMTP(host=smtp_server,
                        port=smtp_port)

    mail.starttls()

    mail.login(user=sender_email,
               password=sender_password)

    mail.sendmail(from_addr=sender_email,
                  to_addrs=[user_name],
                  msg=msg.as_string())

    mail.quit()


##################################################################################
# products functions
##################################################################################
def get_products_by_region(region_id):
    try:
        q = {"region_id": region_id}

        products = mongo.select_from_db(collection_name="products",
                                        query_dict=q)
        products_data = {}

        for product in products:
            category = product['category_name']
            if category not in products_data:
                products_data[category] = []

            product_dict = {"product_id": product["product_id"],
                            "product_name": product["product_name"],
                            "barcode": product.get("barcode", ""),
                            "product_img": product["product_img"]
                            }
            products_data[category].append(product_dict)

        return products_data

    except Exception as e:
        print(e)


def insert_to_cart(user_name, product_id, region_id, quantity):
    try:
        q1 = {"user_name": user_name,
              "product_id": product_id,
              "region_id": region_id}

        docs = mongo.select_from_db(collection_name="carts",
                                    query_dict=q1)

        docs_list = [r for r in docs]

        if len(docs_list) > 0:
            q3 = {'$inc': {'quantity': int(quantity)}}

            mongo.update_db(collection_name="carts",
                            filter_query_dict=q1,
                            update_query_dict=q3)

        else:
            q3 = {"user_name": user_name,
                  "product_id": product_id,
                  "region_id": region_id,
                  "quantity": int(quantity)}

            mongo.insert_to_db(collection_name="carts",
                               query_dict=q3)

    except Exception as e:
        print(e)


def find_product_by_barcode(region_id, barcode):
    try:
        q = {"region_id": region_id,
             "barcode": barcode}

        products = mongo.select_from_db(collection_name="products",
                                        query_dict=q)

        if len(products) > 0:
            barcode_data = [{"product_id": products[0]["product_id"],
                             "product_name": products[0]["product_name"],
                             "barcode": products[0].get("barcode", ""),
                             "product_img": products[0]["product_img"]
                             }]

        else:
            barcode_data = []

        return barcode_data

    except Exception as e:
        print(e)


##################################################################################
# cart functions
##################################################################################
def remove_buyer_products(user_name):
    try:
        q = {"user_name": user_name
             }

        mongo.delete_from_db(collection_name="carts",
                             query_dict=q)

    except Exception as e:
        print(e)


def show_cart(user_name, region_id):
    try:
        q1 = {"user_name": user_name}

        docs = mongo.select_from_db(collection_name="carts",
                                    query_dict=q1)

        cart_list = [{'product_id': r['product_id'], 'quantity': r['quantity']} for r in docs]
        cart_list_fixed = []

        for item in cart_list:
            product_id = item['product_id']

            q2 = {"product_id": product_id,
                  "region_id": region_id}

            docs2 = mongo.select_from_db(collection_name="products",
                                         query_dict=q2)

            for doc in docs2:
                item['product_name'] = doc['product_name']
                item['product_img'] = doc['product_img']

                cart_list_fixed.append(item)

        products_list = []

        if len(cart_list_fixed) > 0:
            for cart in cart_list_fixed:
                product_id = cart["product_id"]

                aggreagate = [
                        {'$match': {
                                'product_id': product_id,
                                'region_id': region_id
                                 }
                         },
                        {
                            '$project': {
                                'product_name': 1,
                                'product_id': 1,
                                'product_img': 1,
                                'stores': {
                                    '$filter': {
                                        'input': '$stores',
                                        'as': 'store',
                                        'cond': {
                                            '$ne': [
                                                '$$store.price', 0
                                            ]
                                        }
                                    }
                                }
                            }
                         },
                        {
                            '$unwind': '$stores'
                         },
                        {
                            '$sort': {
                                'stores.price': 1
                                 }
                        },
                        {
                            '$group': {
                                '_id': {
                                    'product_name': '$product_name',
                                    'product_id': '$product_id',
                                    'product_img': '$product_img'
                                },
                                'stores': {
                                    '$push': '$stores'
                                }
                            }
                        },
                        {
                            '$project': {
                                '_id': 0,
                                'product_name': '$_id.product_name',
                                'product_id': '$_id.product_id',
                                'product_img': '$_id.product_img',
                                'stores': 1
                                 }
                        }
                ]

                result = mongo.aggregate_from_db(collection_name="products",
                                                 query_list=aggreagate)

                products_list.append(result)

            # Create a set to store the store names from the first item in the list
            common_stores = set(products_list[0][0]['stores'][i]['store_name'] for i in range(len(products_list[0][0]['stores'])))

            # Iterate over the remaining items and keep only the common stores
            for item in products_list[1:]:
                stores = item[0]['stores']
                common_stores.intersection_update(store['store_name'] for store in stores)

            # Replace original stores items with the remaining one (max 10 stores)
            for item in products_list:
                stores = item[0]['stores']
                remaining_stores = []

                for store_item in stores:
                    if store_item['store_name'] in common_stores:
                        remaining_stores.append(store_item)

                remaining_stores = sorted(remaining_stores, key=lambda x: x['price'])

                item[0]['stores'] = remaining_stores

            store_total_cost = {}

            # Calculate the total cost for each store in the input list based on the quantity from the cart
            for cart_item in cart_list:
                product_id = cart_item['product_id']
                quantity = cart_item['quantity']

                for product in products_list:
                    for item in product:
                        if item['product_id'] == product_id:
                            stores = item['stores']
                            for store in stores:
                                store_name = store['store_name']
                                price = store['price']
                                if store_name in store_total_cost:
                                    store_total_cost[store_name] += price * quantity
                                else:
                                    store_total_cost[store_name] = price * quantity

            # Create the list of dictionaries containing store name and total cost
            offers = [{'store_name': store, 'total_cost': "%.2f" % ((math.ceil(store_total_cost[store] * 100))/100)} for store
                      in store_total_cost]

            offers = sorted(offers, key=lambda x: x['total_cost'])
            offers = offers[:10]

        else:
            offers = []

        return cart_list_fixed, offers

    except Exception as e:
        print(e)


def update_cart_product(user_name, product_id, region_id, new_quantity):
    q1 = {"user_name": user_name,
          "product_id": product_id,
          "region_id": region_id}

    docs = mongo.select_from_db(collection_name="carts",
                                query_dict=q1)

    docs_list = [r for r in docs]

    if len(docs_list) > 0:
        q3 = {'$set': {'quantity': int(new_quantity)}}

        mongo.update_db(collection_name="carts",
                        filter_query_dict=q1,
                        update_query_dict=q3)


def remove_cart_product(user_name, product_id, region_id,):
    try:
        q = {"user_name": user_name,
             "product_id": product_id,
             "region_id": region_id}

        mongo.delete_from_db(collection_name="carts",
                             query_dict=q)

    except Exception as e:
        print(e)



