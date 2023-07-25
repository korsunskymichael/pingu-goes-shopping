import functools
from flask import Flask, render_template, request, redirect, url_for, session, flash
from static.python.functions import *
from static.python.configs import *
from static.python.credentials import app_secret_key

app = Flask(__name__)
app.secret_key = app_secret_key


@app.route('/')
def index():
    return render_template(template_name_or_list="/html/index.html")


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(*args, **kwargs):
        if 'user_name' not in session:
            return redirect('/')

        return view(*args, **kwargs)

    return wrapped_view


@app.route(rule='/logout')
def logout():
    user_name = session['user_name']
    remove_buyer_products(user_name=user_name)

    # Clear the session data
    session.clear()

    return redirect(location=url_for(endpoint='index'))


@app.route(rule='/login', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        user_name = request.form["username"]
        user_password = request.form["password"]
        valid_user, user_name = check_auth_user(user_name=user_name,
                                                user_password=user_password)

        if valid_user:
            session['user_name'] = user_name

            return redirect(location=url_for(endpoint="show_regions"))

        else:
            flash(message="שגיאה בחיבור, אנא הזן שם משתמש וסיסמא נכונים!")

            return redirect(location=url_for(endpoint="login"))

    return render_template(template_name_or_list="/html/login.html")


@app.route(rule='/password_recovery', methods=['POST'])
def password_recovery():
    if request.method == "POST":
        user_name = request.form["recovery_username"]

        password = get_user_password(user_name=user_name)

        if password != '':
            send_password_recovery(user_name=user_name,
                                   password=password)

        else:
            flash(message="לא נמצא שם משתמש, אנא הזן שם משתמש תקין!")
            return redirect(location=url_for(endpoint="login"))

    return redirect(location=url_for(endpoint="login"))


@app.route('/signup', methods=["POST", "GET"])
def signup():
    if request.method == "POST":
        user_name = request.form['username']
        user_password = request.form["password"]
        exists = check_if_user_exists(user_name=user_name)

        for mail_suffix in allowed_mail_suffixes:
            if user_name.endswith(mail_suffix) is True:
                if exists is False:
                    add_user(user_name=user_name,
                             user_password=user_password)

                    return redirect(location=url_for(endpoint="login"))

                else:
                    flash(message="השם משתמש שהוזן כבר קיים במערכת, אנא הזן שם משתמש שונה!")
                    return redirect(location=url_for(endpoint="signup"))

        flash(message=" 'gmail.com' או 'walla.co.il' סיומת מייל לא תקנית, סיומות מייל אפשריות הן  ")
        return redirect(location=url_for(endpoint="signup"))

    return render_template(template_name_or_list='/html/signup.html')


@app.route('/regions', methods=['POST', 'GET'])
@login_required
def show_regions():
    user_name = session['user_name']
    remove_buyer_products(user_name=user_name)

    return render_template(template_name_or_list="/html/regions.html")


@app.route('/products', methods=['POST', 'GET'])
@login_required
def products():
    region = request.form.get('region', '')

    if region != '':
        session['chosen_region'] = region

    else:
        region = session['chosen_region']

    region_id = regions[region]

    products_data = get_products_by_region(region_id=region_id)

    return render_template(template_name_or_list='/html/products.html',
                           products_data=products_data,
                           barcode_data=[])


@app.route('/close_barcode', methods=['POST', 'GET'])
def close_barcode_window():
    if request.method == "POST":
        region = session['chosen_region']
        region_id = regions[region]

        products_data = get_products_by_region(region_id=region_id)

        return render_template(template_name_or_list='/html/products.html',
                               products_data=products_data,
                               barcode_data=[])


@app.route('/search_barcode', methods=['POST', 'GET'])
@login_required
def find_product():
    barcode = request.form.get('barcode', '')

    if barcode != '':
        region = session['chosen_region']

        region_id = regions[region]

        products_data = get_products_by_region(region_id=region_id)
        barcode_data = find_product_by_barcode(region_id=region_id,
                                               barcode=barcode)

        if len(barcode_data) > 0:

            return render_template(template_name_or_list='/html/products.html',
                                   products_data=products_data,
                                   barcode_data=barcode_data)

        else:
            flash("ברקוד לא תקין, אנא נסה שנית!")
            return render_template(template_name_or_list='/html/products.html',
                                   products_data=products_data,
                                   barcode_data=[])


@app.route('/add_to_cart', methods=['POST'])
def add_to_cart():
    product_id = request.form.get('product_id')
    quantity = request.form.get('quantity')
    user_name = session['user_name']
    region_id = regions[session['chosen_region']]

    insert_to_cart(user_name=user_name,
                   product_id=product_id,
                   region_id=region_id,
                   quantity=quantity)

    return redirect(location=url_for(endpoint='products'))


@app.route('/view_cart')
@login_required
def view_cart():
    user_name = session['user_name']
    region_id = regions[session['chosen_region']]

    cart_list, offers = show_cart(user_name=user_name,
                                  region_id=region_id)

    return render_template(template_name_or_list='/html/cart.html',
                           cart_list=cart_list,
                           offers=offers)


@app.route('/clear_cart')
def clear_cart():
    remove_buyer_products(user_name=session['user_name'])
    return redirect(location=url_for(endpoint='products'))


@app.route('/update_cart_product', methods=['POST'])
def update_product_quantity():
    if request.method == "POST":
        product_id = request.form.get('product_id')
        new_quantity = request.form.get('quantity')
        user_name = session['user_name']
        region_id = regions[session['chosen_region']]

        update_cart_product(user_name=user_name,
                            product_id=product_id,
                            region_id=region_id,
                            new_quantity=new_quantity)

        return redirect(location=url_for(endpoint='view_cart'))


@app.route('/delete_cart_product', methods=['POST'])
def remove_product_from_cart():
    if request.method == "POST":
        product_id = request.form.get('product_id')
        user_name = session['user_name']
        region_id = regions[session['chosen_region']]

        remove_cart_product(user_name=user_name,
                            product_id=product_id,
                            region_id=region_id)

        return redirect(location=url_for(endpoint='view_cart'))


if __name__ == '__main__':
    app.run(debug=True)
    # app.run(host='0.0.0.0', port=81, debug=True) # to run in replit.com,
    # also change the name of file to main.py if you are using replit.com
