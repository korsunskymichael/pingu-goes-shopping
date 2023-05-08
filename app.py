from flask import Flask, render_template, request, redirect, url_for, session
from static.python.functions import *
import functools

app = Flask(__name__)
app.secret_key = '12358'


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(*args, **kwargs):
        if 'user_name' not in session:
            return redirect('/')
        return view(*args, **kwargs)
    return wrapped_view


@app.route('/')
def index():
    return render_template("/html/index.html")


@app.route('/logout')
def logout():
    # Clear the session data
    session.clear()
    return redirect(url_for('index'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        user_name = request.form["username"]
        user_password = request.form["password"]
        valid_user, user_name = check_auth_user(user_name, user_password)

        if valid_user:
            session['user_name'] = user_name
            return redirect(url_for("products"))
        else:
            print("incorrect user or password")
            return redirect(url_for("login"))

    return render_template("/html/login.html")


@app.route('/signup', methods=["POST", "GET"])
def signup():
    if request.method == "POST":
        user_name = request.form['username']
        user_password = request.form["password"]
        usernames = get_users()

        if user_name not in usernames:
            add_user(user_name, user_password)
            return redirect(url_for("login"))
        
        else:
            print("user name already exist")
            return redirect(url_for("signup"))

    return render_template('/html/signup.html')


@app.route('/products')
def products():
    products = get_product_names()
    return render_template('/html/products.html', products=products)


@app.route('/add_to_cart', methods=['POST'])
def add_to_cart():
    product_id = request.form.get('product_id')
    quantity = request.form.get('quantity')

    insert_to_cart(user_name=session['user_name'],
                   product_id=product_id,
                   quantity=quantity)

    return redirect(url_for('products'))


@app.route('/view_cart')
def view_cart():
    cart = show_cart(user_name=session['user_name'])
    return render_template('/html/cart.html', carts=cart)


@app.route('/clear_cart')
def clear_cart():
    remove_buyer_products(user_name=session['user_name'])
    return redirect(url_for('products'))


@app.route('/home')
def redirect_home():
    return redirect(url_for('products'))


@app.route('/best_offer')
def best_offer():
    offers = get_best_offers(user_name=session['user_name'])
    return render_template('/html/best_offer.html', offers=offers)


if __name__ == '__main__':
    execute_queries_from_file('static/sql/db_init.sql')
    execute_queries_from_file('static/sql/insert_values.sql')

    app.run(debug=True)
