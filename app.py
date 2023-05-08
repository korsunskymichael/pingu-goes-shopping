from flask import Flask, render_template, request, redirect, url_for
from static.python.functions import *

app = Flask(__name__)

buyer_id = '12358'


@app.route('/')
def home():
    products = get_product_names()
    return render_template('/html/index.html', products=products)


@app.route('/add_to_cart', methods=['POST'])
def add_to_cart():
    product_id = request.form.get('product_id')
    quantity = request.form.get('quantity')

    insert_to_cart(buyer_id=buyer_id,
                   product_id=product_id,
                   quantity=quantity)

    return redirect(url_for('home'))


@app.route('/view_cart')
def view_cart():
    cart = show_cart(buyer_id=buyer_id)
    return render_template('/html/cart.html', carts=cart)


@app.route('/clear_cart')
def clear_cart():
    remove_buyer_products(buyer_id=buyer_id)
    return redirect(url_for('home'))


@app.route('/home')
def redirect_home():
    return redirect(url_for('home'))


@app.route('/best_offer')
def best_offer():
    offers = get_best_offers(buyer_id=buyer_id)
    return render_template('/html/best_offer.html', offers=offers)


if __name__ == '__main__':
    connection = sqlite3.connect(DATABASE)

    path = 'static/sql/db_init.sql'
    queries_str = open(path, 'r').read()
    queries = queries_str.replace('\n', '').split(';')
    queries = [query.strip() for query in queries if query != '']

    for q in queries:
        cursor = connection.cursor()
        cursor.execute(q)

    path = 'static/sql/insert_values.sql'
    q = open(path, 'r').read()
    queries_str = open(path, 'r').read()
    queries = queries_str.replace('\n', '').split(';')
    queries = [query.strip() for query in queries if query != '']

    for q in queries:
        cursor = connection.cursor()
        cursor.execute(q)

    connection.commit()
    connection.close()

    app.run(debug=True)
