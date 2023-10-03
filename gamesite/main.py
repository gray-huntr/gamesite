
# import app as app
import os

import app as app
from flask import *
import pymysql
from uuid import uuid4
# from werkzeug.utils import redirect
from werkzeug.utils import secure_filename

app.secret_key = "Wdg@#$%89jMfh2879mT"

app = Flask(__name__)
from flask import request
import redirect

# Route for the home page
@app.route('/home')
def home():
    return render_template('home.html')
# route for the index page (Signup)
@app.route('/', methods=['POST','GET'])
def sign_up():
    if request.method == 'POST':
        username = request.form['username']
        name = request.form['name']
        phone = request.form['phone']
        email = request.form['email']
        location = request.form['location']
        password = request.form['password']
        rep_pass = request.form['repeat_pass']
        # first connect to local host and game store database
        conn = pymysql.connect(host="localhost", user="root", password="", database="game_store")        
        cursor = conn.cursor()
        # Check first whether there is an already existing account
        cursor.execute("select * from clients where username = '{}' ".format(username))
        if cursor.rowcount == 1:
            return render_template('sign_up.html', msg="Username already exists")
        else:
            # if there is no existing account, check whether the two passwords match
            if password == rep_pass:
                # we first connect to local host and gamestore database
                conn = pymysql.connect(host="localhost", user="root", password="", database="game_store")
                #     insert the records to the users tables
                cursor = conn.cursor()
                cursor.execute(
                    "insert into clients(username,name,phone,email,location,password) values (%s,%s,%s,%s,%s,%s)",
                    (username, name, phone, email, location, password))
                    # save records
                conn.commit()
                # redirect them to login page
                return render_template('users_login.html', )
                # if passwords do not match display the following message
            elif password != rep_pass:
                return render_template('sign_up.html', msg="Passwords do not match")
            else:
                return render_template('sign_up.html', msg="Error")
    else:
        return render_template('sign_up.html')

# Route for the tournaments page (admin side)
@app.route('/tournaments')
def tournaments():
    return render_template('tournaments.html')
# Route for the paybill page incase mpesa stk push fails
@app.route('/paybill')
def paybill():
    return render_template('paybill.html')

@app.route('/admin', methods=['POST','GET'])
def admin():
    return render_template('admin.html')

@app.route('/admin_signup', methods=['POST','GET'])
def admin_signup():
    if request.method == 'POST':
        username = request.form['username']
        name = request.form['name']
        phone = request.form['phone']
        email = request.form['email']
        password = request.form['password']
        rep_pass = request.form['repeat_pass']

        if password == rep_pass:

            # we first connect to local host and gamestore database
             conn = pymysql.connect(host="localhost", user="root", password="", database="game_store")
    #     insert the records to the users tables i.e email and password
             cursor = conn.cursor()
             cursor.execute("insert into admins(username,name,phone,email,password) values (%s,%s,%s,%s,%s)", (username,name,phone,email, password))
             conn.commit()
             return render_template('admin_signup.html', msg="User registered successfully" )
        elif password != rep_pass:
            return render_template('admin_signup.html', msg="Passwords do not match")
        else:
            return render_template('admin_signup.html', msg="Error")
    else:
         return render_template('admin_signup.html')

@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/users_login', methods=['POST', 'GET'])
def users_login():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']

        # We first connect to local host and the gamestore database
        conn = pymysql.connect(host="localhost", user="root", password="", database="game_store")

        # pick the record from the clients table
        cursor = conn.cursor()
        cursor.execute("select * from clients where username =%s and password=%s", (username, password))
        if cursor.rowcount ==1:
            if cursor.rowcount == 1:
                # Check if page is in session
                if 'page' in session:
                    # if page is in session and is mpesa, proceed with the following
                    if session['page'] == 'mpesa':
                        # assign a key session from the username
                        session['username'] = username
                        # remove the page session
                        session.pop('page', None)
                        # Redirect to the mpesa page
                        return redirect('/mpesa_payment')
                    elif session['page'] == 'checkout':
                        session['username'] = username
                        session.pop('page', None)
                        return redirect('/cart')
                    elif session['page'] == 'tournament':
                        session['username'] = username
                        session.pop('page', None)
                        return redirect('/new_arrivals')
                # if page is not in session, redirect to the home page
                else:
                    session['username'] = username
                    return redirect('/home')
            elif cursor.rowcount == 0:
                return render_template('users_login.html', msg="User does not exist or incorrect password")

        elif cursor.rowcount ==0:
            cursor = conn.cursor()
            cursor.execute("select * from admins where username =%s and password=%s", (username, password))
            if cursor.rowcount == 1:
                return render_template('admin.html', msg="login successful")
            elif cursor.rowcount == 0:
                return render_template('users_login.html', msg="User does not exist or incorrect password")
    else:
        return render_template('users_login.html')

@app.route('/reset_password', methods=['POST', 'GET'])
def reset_password():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        rep_pass = request.form['rep_password']
        # we first connect to local host and gamestore database
        conn = pymysql.connect(host="localhost", user="root", password="", database="game_store")
        #     insert the records to the users tables i.e email and password
        cursor = conn.cursor()
        cursor.execute("select * from clients where username = '{}'".format(username))

        if cursor.rowcount == 1:
            if password == rep_pass:

                # we first connect to local host and gamestore database
                conn = pymysql.connect(host="localhost", user="root", password="", database="game_store")
                #     insert the records to the users tables i.e email and password
                cursor = conn.cursor()
                cursor.execute("UPDATE clients SET password = '{}' WHERE username = '{}' ".format(password, username))
                conn.commit()
                return render_template('reset_password.html', msg="Password reset, Login to continue")
            elif password != rep_pass:
                return render_template('reset_password.html', msg="Passwords do not match")
            else:
                return render_template('reset_password.html', msg="Error")
        else:
            if password == rep_pass:

                # we first connect to local host and gamestore database
                conn = pymysql.connect(host="localhost", user="root", password="", database="game_store")
                #     insert the records to the users tables i.e email and password
                cursor = conn.cursor()
                cursor.execute("UPDATE admins SET password = '{}' WHERE username = '{}' ".format(password, username))
                conn.commit()
                return render_template('reset_password.html', msg="Password reset, Login to continue")
            elif password != rep_pass:
                return render_template('reset_password.html', msg="Passwords do not match")
            else:
                return render_template('reset_password.html', msg="Error")
    else:
        return render_template('reset_password.html')


@app.route('/games')
def games():
    # connect to database
    conn = pymysql.connect(host="localhost", user="root", password="", database="game_store")
    cursor = conn.cursor()
    # Execute the query using the cursor
    cursor.execute("select * from games")
    # Check for records
    if cursor.rowcount == 0:
        return render_template('games.html', msg="Out of stock")
    else:
        # return all rows found
        rows = cursor.fetchall()
        return render_template('games.html', rows=rows)


@app.route('/tech')
def tech():
    # connect to database
    conn = pymysql.connect(host="localhost", user="root", password="", database="game_store")
    cursor = conn.cursor()
    # Execute the query using the cursor
    cursor.execute("select * from tech")
    # Check for records
    if cursor.rowcount == 0:
        return render_template('tech.html', msg="Out of stock")
    else:
        # return all rows found
        rows = cursor.fetchall()
        return render_template('tech.html', rows=rows)


@app.route('/contacts')
def contacts():
    return render_template('contacts.html')


@app.route('/new_arrivals', methods=['POST', 'GET'])
def new_arrivals():
    conn = pymysql.connect(host="localhost", user="root", password="", database="game_store")
    cursor = conn.cursor()
    # execute the query using the cursor
    cursor.execute("select * from new_arrivals")       
        # check for records
    if cursor.rowcount == 0:
        return render_template('new_arrivals.html', msg="NO PRODUCTS AVAILABLE YET ")
    elif cursor.rowcount >= 1:
        rows = cursor.fetchall()
        if request.method == 'POST':
            # check if the username is in session
            if 'username' in session:
                username = session['username']
                name = request.form['full_name']
                number = request.form['phone_number']
                email = request.form['email']
                game = request.form['GOC']
                conn = pymysql.connect(host="localhost", user="root", password="", database="game_store")
                #     insert the records to the Tournaments tables
                cursor = conn.cursor()
                cursor.execute("insert into tournaments(username,name,number,email,game) values (%s,%s,%s,%s,%s)",
                                (username, name, number, email, game,))
                conn.commit()
                return render_template('new_arrivals.html', msg="Application submitted successfully", rows=rows)
            # if username is not in session, create a page session, name it tournament and redirect to the signin page
            else:
                session['page'] = 'tournament'
                return redirect ('/users_login')

        else:
            return render_template('new_arrivals.html', rows=rows)


@app.route('/purchase_games/<id>')
def purchase_games(id):
    conn = pymysql.connect(host="localhost", user="root", password="", database="game_store")
    cursor = conn.cursor()
    # execute the query using the cursor
    cursor.execute("select * from games where product_id = %s", (id))
    # check for records
    if cursor.rowcount == 0:
        return render_template('purchase_games.html', msg="This product does not exist")
    else:
        # return all rows found
        rows = cursor.fetchall()
        for row in rows:
            # stock represents the number of items available in the database
            stock = row[5]
            return render_template('purchase_games.html', rows=rows, stock=stock)


@app.route('/purchase_tech/<id>')
def purchase_tech(id):
    conn = pymysql.connect(host="localhost", user="root", password="", database="game_store")
    cursor = conn.cursor()
    # execute the query using the cursor
    cursor.execute("select * from tech where product_id = %s", (id))
    # check for records
    if cursor.rowcount == 0:
        return render_template('purchase_tech.html', msg="This product does not exist")
    else:
        # return all rows found
        rows = cursor.fetchall()
        for row in rows:
            stock = row[4]
            return render_template('purchase_tech.html', rows=rows, stock=stock)

# random string generator function
def ordercode():
    ident = uuid4().__str__()[:8]
    return f"{ident}"
from flask import redirect, url_for

@app.route('/add/<section>', methods=['POST'])
def add(section):
    # section is recieved as a parameter from the purchase_games or purchase_tech pages
    # if the section is games it follows the below order
    if section == "games":
        # Retrieve information from the form on the page
        id = request.form['id']
        status = request.form['status']
        qtty = int(request.form['qtty'])

        # create a unique code from the random string generator route
        code = ordercode()
        # Connect to the DB
        conn = pymysql.connect(host="localhost", user="root", password="", database="game_store")
        cursor = conn.cursor()
        cursor.execute("select * from games where product_id = '{}'".format(id))
        if cursor.rowcount == 1:
            rows = cursor.fetchall()
            for row in rows:
                # stock represents the number of items available
                # qtty represents the number a user has input
                stock = row[5]
                if qtty > stock:
                    flash("You have input a quantity that is more than the ones remaining")
                    return redirect(f'/purchase_games/{id}')
                elif qtty<= stock:
                    new_stock = stock - qtty
                    cursor.execute("update games set quantity = %s where product_id = %s", (new_stock, id))
                    conn.commit()

        # validate the received values
        if id and request.method == 'POST':
            connection = pymysql.connect(host='localhost', user='root', password='',
                                         database='game_store')
            cursor = connection.cursor(pymysql.cursors.DictCursor)
            cursor.execute("SELECT * FROM games WHERE product_id= %s", id)
            row = cursor.fetchone()

            # An array is a collection of items stored at contiguous memory locations. The idea is to store multiple items of the same type together
            # am item array is created from the data above fetched from the database
            # it is under the random string generated with the route above
            itemArray = {str(code): {'product_name': row['name'], 'product_id': row['product_id'],
                                                  'product_cost': row['cost'],'quantity': qtty,'individual_price': 1 * row['cost'],
                                                  'status': status,'total_price': int(qtty) * row['cost'], 'ordercode':code }}
            # print the item array on the terminal, can be removed....
            # print((itemArray))

            all_total_price = 0
            all_total_quantity = 0
            session.modified = True
            # if there is an item already
            if 'cart_item' in session:
                # a new product added in the cart to Merge the previous to have a new cart item with two products
                session['cart_item'] = array_merge(session['cart_item'], itemArray)
                #  for each item in the array
                for key, value in session['cart_item'].items():
                    individual_quantity = 1
                    individual_total_price = session['cart_item'][key]['total_price']
                    all_total_quantity = all_total_quantity + individual_quantity
                    all_total_price = all_total_price + individual_total_price


            else:
                # if the cart is empty you add the whole item array and create a session
                session['cart_item'] = itemArray
                all_total_quantity = all_total_quantity + 1
                # get total price by multiplyin the cost and the quantity
                all_total_price = all_total_price + int(qtty) * row['cost']

            # add total quantity and total price to a session
            session['all_total_quantity'] = all_total_quantity
            session['all_total_price'] = all_total_price

            return redirect(url_for('.cart'))
        else:
            return 'Error while adding item to cart'
    elif section == "tech":
        # session['section'] = 'games'
        id = request.form['id']
        status = request.form['status']
        qtty = int(request.form['qtty'])

        code = ordercode()

        conn = pymysql.connect(host="localhost", user="root", password="", database="game_store")
        cursor = conn.cursor()
        cursor.execute("select * from tech where product_id = '{}'".format(id))
        if cursor.rowcount == 1:
            rows = cursor.fetchall()
            for row in rows:
                stock = row[4]
                if qtty > stock:
                    flash("You have input a quantity that is more than the ones remaining")
                    return redirect(f'/purchase_tech/{id}')
                elif qtty <= stock:
                    new_stock = stock - qtty
                    cursor.execute("update tech set quantity = %s where product_id = %s", (new_stock, id))
                    conn.commit()

        # validate the received values
        if id and request.method == 'POST':
            connection = pymysql.connect(host='localhost', user='root', password='',
                                         database='game_store')
            cursor = connection.cursor(pymysql.cursors.DictCursor)
            cursor.execute("SELECT * FROM tech WHERE product_id= %s", id)
            row = cursor.fetchone()

            # An array is a collection of items stored at contiguous memory locations. The idea is to store multiple items of the same type together

            itemArray = {code: {'product_name': row['name'], 'product_id': row['product_id'],
                                'product_cost': row['cost'], 'quantity': qtty, 'individual_price': 1 * row['cost'],
                                'status': status, 'total_price': int(qtty) * row['cost'], 'ordercode': code}}
            print((itemArray))

            all_total_price = 0
            all_total_quantity = 0
            session.modified = True
            # if there is an item already
            if 'cart_item' in session:
                # a new product added in the cart.Merge the previous to have a new cart item with two products
                session['cart_item'] = array_merge(session['cart_item'], itemArray)

                for key, value in session['cart_item'].items():
                    individual_quantity = 1
                    individual_total_price = session['cart_item'][key]['total_price']
                    all_total_quantity = all_total_quantity + individual_quantity
                    all_total_price = all_total_price + individual_total_price


            else:
                # if the cart is empty you add the whole item array
                session['cart_item'] = itemArray
                all_total_quantity = all_total_quantity + 1
                # get total price by multiplyin the cost and the quantity
                all_total_price = all_total_price + int(qtty) * row['cost']

            # add total quantity and total price to a session
            session['all_total_quantity'] = all_total_quantity
            session['all_total_price'] = all_total_price

            return redirect(url_for('.cart'))
        else:
            return 'Error while adding item to cart'

@app.route('/cart')
def cart():
    return render_template('cart.html')


def array_merge(first_array, second_array):
    if isinstance(first_array, list) and isinstance(second_array, list):
        return first_array + second_array
    # takes the new product add to the existing and merge to have one array with two products
    elif isinstance(first_array, dict) and isinstance(second_array, dict):
        return dict(list(first_array.items()) + list(second_array.items()))
    elif isinstance(first_array, set) and isinstance(second_array, set):
        return first_array.union(second_array)
    return False

# Route to empty the cart
@app.route('/empty')
def empty_cart():
    try:
        for key, value in session['cart_item'].items(): #takes and processes all the items in the cart item array
            # Each variable represents a particular session that is in the cart item
            ordercode =  session['cart_item'][key]['ordercode']
            id = session['cart_item'][key]['product_id']
            quantity =  session['cart_item'][key]['quantity']
            for item in session['cart_item'].items():
                # for each item in the cart item array check whether the value at index 0 is equal to the order code
                if item[0] == ordercode:
                    conn = pymysql.connect(host="localhost", user="root", password="", database="game_store")
                    cursor = conn.cursor()
                    cursor.execute("select * from games where product_id = '{}'".format(id))
                    # first checks if the id matches with any data in the games table, if it matches,it will take the below route, if not.....else route
                    if cursor.rowcount == 1:
                        rows = cursor.fetchall()
                        # if the cart is emptied, the quantity of each item in the item array is reverted back to its original number before it was added to cart
                        for row in rows:
                            stock = row[5]
                            new_stock = stock + int(quantity)
                            cursor.execute("update games set quantity = %s where product_id = %s", (new_stock, id))
                            conn.commit()
                    else:
                        cursor.execute("select * from tech where product_id = '{}'".format(id))
                        rows = cursor.fetchall()
                        for row in rows:
                            stock = row[4]
                            new_stock = stock + int(quantity)
                            cursor.execute("update tech set quantity = %s where product_id = %s", (new_stock, id))
                            conn.commit()

        # after all the emptying is done, the function clears the below sessions leaving the cart empty
        if 'cart_item' in session or 'all_total_quantity' in session or 'all_total_price' in session:
            session.pop('cart_item', None)
            session.pop('all_total_quantity', None)
            session.pop('all_total_price', None)
            return redirect(url_for('.cart'))
        else:
            return redirect(url_for('.cart'))

    except Exception as e:
        print(e)
@app.route('/delete/<string:code>/<int:quantity>/<string:id>')
def delete_product(code,quantity,id):
    try:
        all_total_price = 0
        all_total_quantity = 0
        session.modified = True
        for item in session['cart_item'].items():
            if item[0] == code:
                conn = pymysql.connect(host="localhost", user="root", password="", database="game_store")
                cursor = conn.cursor()
                cursor.execute("select * from games where product_id = '{}'".format(id))
                if cursor.rowcount == 1:
                    rows = cursor.fetchall()
                    for row in rows:
                        stock = row[5]
                        new_stock = stock + int(quantity)
                        cursor.execute("update games set quantity = %s where product_id = %s", (new_stock, id))
                        conn.commit()
                else:
                    cursor.execute("select * from tech where product_id = '{}'".format(id))
                    rows = cursor.fetchall()
                    for row in rows:
                        stock = row[4]
                        new_stock = stock + int(quantity)
                        cursor.execute("update tech set quantity = %s where product_id = %s", (new_stock, id))
                        conn.commit()

                session['cart_item'].pop(item[0], None)
                if 'cart_item' in session:
                    for key, value in session['cart_item'].items():
                        #individual_quantity = int(session['cart_item'][key]['quantity'])
                        individual_total_price = session['cart_item'][key]['total_price']
                        all_total_quantity = all_total_quantity + 1
                        all_total_price = all_total_price + individual_total_price
                break

        if all_total_quantity == 0:
            session.pop('cart_item', None)
        else:
            session['all_total_quantity'] = all_total_quantity
            session['all_total_price'] = all_total_price
        return redirect(url_for('.cart'))

    except Exception as e:
        print(e)





@app.route('/checkout', methods=['POST', 'GET'])
def checkout( ):
    if 'username' in session:
        if 'cart_item' in session:
            all_total_price = 0
            all_total_quantity = 0
            for key, value in session['cart_item'].items():
                individual_quantity = 1
                individual_total_price = session['cart_item'][key]['total_price']
                ordercode =  session['cart_item'][key]['ordercode']
                id = session['cart_item'][key]['product_id']
                name =  session['cart_item'][key]['product_name']
                user_name = session['username']
                status = session['cart_item'][key]['status']
                cost = session['cart_item'][key]['product_cost']
                qtty =  session['cart_item'][key]['quantity']
                total =session['cart_item'][key]['total_price']

                all_total_quantity = all_total_quantity + individual_quantity
                all_total_price = all_total_price + individual_total_price

                username = session['username']
                # session
                if not username:
                    return redirect('/signin')
                elif not individual_total_price or not individual_quantity or not id or not name or not all_total_price or not all_total_quantity:
                    return redirect('/cart')
                else:
                    # we first connect to local host and game_store database
                    conn = pymysql.connect(host="localhost", user="root", password="", database="game_store")
                    #     insert the records to the orders tables
                    cursor = conn.cursor()
                    cursor.execute(
                        "insert into orders(order_code,id,name,cost,quantity,total,r_name,status) values('{}','{}','{}','{}','{}','{}','{}','{}')".format(
                            ordercode,id, name, cost, qtty, total, user_name, status))
                    conn.commit()
            session.pop('cart_item', None)
            session.pop('all_total_quantity', None)
            session.pop('all_total_price', None)
            session.pop('page', None)
            return render_template('cart.html', msg='Your order(s) have been placed successfully and will be delivered to you ')
    else:
        session['page'] = "checkout"
        return redirect ('/users_login')

@app.route("/my_orders", methods=['POST', 'GET'])
def orders():
    if 'username' in session:

        conn = pymysql.connect(host="localhost", user="root", password="", database="game_store")
        cursor = conn.cursor()
        cursor.execute("select * from orders where r_name = '{}'".format(session['username']))

        if cursor.rowcount == 0:
            return render_template('my_orders.html', msg="Your cart is empty")
        else:

            rows = cursor.fetchall()
            # get total
            total_sum = 0
            for row in rows:
                total_sum = total_sum + row[6]
            return render_template('my_orders.html', rows=rows, total_sum=total_sum)
    else:
        return redirect('/users_login')



@app.route("/remove/<id>/<order_code>/<quantity>", methods=['POST', 'GET'])
def remove(id,order_code,quantity):
    # if request.method == 'POST':
    #     id = request.form['product_id']

            conn = pymysql.connect(host="localhost", user="root", password="", database="game_store")
            cursor = conn.cursor()
            cursor.execute("DELETE FROM orders WHERE order_code = '{}' and r_name = '{}'".format(order_code,session['username']))
            conn.commit()

            cursor.execute("select * from games where product_id = '{}'".format(id))
            if cursor.rowcount ==1:
                rows = cursor.fetchall()
                for row in rows:
                    stock = row[5]
                    new_stock = stock + int(quantity)
                    cursor.execute("update games set quantity = %s where product_id = %s", (new_stock, id))
                    conn.commit()
            else:
                cursor.execute("select * from tech where product_id = '{}'".format(id))
                rows = cursor.fetchall()
                for row in rows:
                    stock = row[4]
                    new_stock = stock + int(quantity)
                    cursor.execute("update tech set quantity = %s where product_id = %s", (new_stock, id))
                    conn.commit()

            return redirect('/mycart')

@app.route('/complete/<id>', methods=['POST', 'GET'])
def update(id):
        # we first connect to local host and game_store database
        conn = pymysql.connect(host="localhost", user="root", password="", database="game_store")
        #     insert the records to the orders tables
        cursor = conn.cursor()
        cursor.execute("UPDATE orders SET status = 'COMPLETE' WHERE order_code = '{}' ".format(id))
        conn.commit()
        return redirect('/all_orders')

@app.route('/cancelled/<id>', methods=['POST', 'GET'])
def cancelled(id):

        # we first connect to local host and game_store database
        conn = pymysql.connect(host="localhost", user="root", password="", database="game_store")
        #     insert the records to the orders tables
        cursor = conn.cursor()
        cursor.execute("UPDATE orders SET status = 'CANCELLED' WHERE order_code = '{}' ".format(id))
        conn.commit()
        return redirect('/all_orders')

@app.route('/order_search', methods=['POST', 'GET'])
def order_search():
    if request.method == 'POST':
        id = request.form['order_id']

        conn = pymysql.connect(host="localhost", user="root", password="", database="game_store")
        #     insert the records to the products tables
        cursor = conn.cursor()
        cursor.execute("select * from orders where order_code like'{}' OR order_number like '{}'".format(id,id))

        if cursor.rowcount == 0:
            return render_template('all_records.html', msg='ORDER CODE/NUMBER DOES NOT EXIST')
        else:
            rows = cursor.fetchall()
            return render_template('all_records.html', rows=rows)
    else:
        return render_template('all_records.html')

@app.route('/admin_update', methods=['POST', 'GET'])
def admin_update():
    if request.method == 'POST':
        email = request.form['email']
        name = request.form['name']
        username = request.form['username']
        phone = request.form['number']
        password = request.form['password']
        rep_pass = request.form['rep_pass']

        if password == rep_pass:
            # we first connect to local host and game_store database
            conn = pymysql.connect(host="localhost", user="root", password="", database="game_store")
            #     insert the records to the table
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE admins SET name = '{}',username = '{}',phone = '{}', password = '{}' WHERE email = '{}' ".format(name,username,
                                                                                                         phone,
                                                                                                         password,
                                                                                                         email))
            conn.commit()
            return render_template('admin_update.html', msg="Records updated successfully")
        else:
            return render_template('admin_update.html', msg="Passwords do not match")
    else:
        return render_template('admin_update.html')

@app.route('/client_update', methods=['POST', 'GET'])
def client_update():
    if 'username' in session:
        if request.method == 'POST':
            email = request.form['email']
            username = request.form['username']
            name = request.form['name']
            phone = request.form['number']
            location = request.form['location']
            password = request.form['password']
            rep_pass = request.form['rep_pass']


            if password == rep_pass:
                # we first connect to local host and game_store database
                conn = pymysql.connect(host="localhost", user="root", password="", database="game_store")
                #     insert the records to the products tables
                cursor = conn.cursor()
                cursor.execute(
                    "UPDATE clients SET name = '{}',username = '{}',phone = '{}',location = '{}', password = '{}' WHERE email = '{}' ".format(
                        name, username,
                        phone, location,
                        password,
                        email))
                conn.commit()
                return render_template('client_update.html', msg="Records updated successfully")
            else:
                return render_template('client_update.html', msg="Passwords do not match")
        else:
            return render_template('client_update.html')
    else:
        return redirect ('/users_login')
@app.route('/client_records', methods=['POST', 'GET'])
def client_records():

        # we first connect to local host and game_store database
    conn = pymysql.connect(host="localhost", user="root", password="", database="game_store")
    #     insert the records to the products tables
    cursor = conn.cursor()
    cursor.execute("select * from clients" )
    if cursor.rowcount == 0:
        return render_template('client_records.html', msg="No users available")
    else:
        rows = cursor.fetchall()
        return render_template('client_records.html', rows=rows)

@app.route('/client_search_records', methods=['POST', 'GET'])
def client_search_records():
    if request.method == 'POST':
        email = request.form['email']
        conn = pymysql.connect(host="localhost", user="root", password="", database="game_store")
        #     insert the records to the products tables
        cursor = conn.cursor()
        cursor.execute("select * from clients where email = '{}'".format(email))

        if cursor.rowcount == 0:
            return render_template('client_records.html', msg='Client does not exist')

        else:
            rows = cursor.fetchall()
            print (rows)
            return render_template('client_records.html', rows=rows)
    else:
        return render_template('client_records.html')

@app.route('/all_orders', methods=['POST', 'GET'])
def all_orders():
    conn = pymysql.connect(host="localhost", user="root", password="", database="game_store")
    #     insert the records to the products tables
    cursor = conn.cursor()
    cursor.execute("select * from orders")

    if cursor.rowcount == 0:
        return render_template('all_records.html', msg='NO ORDER RECORDS AVAILABLE')
    else:
        rows = cursor.fetchall()
        # print (rows)
        return render_template('all_records.html', rows=rows)

@app.route('/games_search', methods=['POST', 'GET'])
def games_search():
    if request.method == 'POST':
        name = request.form['games_search']

        conn = pymysql.connect(host="localhost", user="root", password="", database="game_store")
        #     insert the records to the products tables
        cursor = conn.cursor()
        cursor.execute("select * from games where name = '{}'".format(name))

        if cursor.rowcount == 0:
            return render_template('games.html', msg='NO RESULTS')
        else:
            rows = cursor.fetchall()
            print (rows)
            return render_template('games.html', rows=rows)
    else:
        return render_template('games.html')

@app.route('/tech_search', methods=['POST', 'GET'])
def tech_search():
    if request.method == 'POST':
        name = request.form['tech_search']

        conn = pymysql.connect(host="localhost", user="root", password="", database="game_store")
        #     insert the records to the products tables
        cursor = conn.cursor()
        cursor.execute("select * from tech where name = '{}'".format(name))

        if cursor.rowcount == 0:
            return render_template('tech.html', msg='NO RESULTS')
        else:
            rows = cursor.fetchall()
            print(rows)
            return render_template('tech.html', rows=rows)
    else:
        return render_template('tech.html')

@app.route('/add_games', methods=['POST', 'GET'])
def add_games():
    if request.method == 'POST':
        product_id = request.form['product_id']
        name = request.form['name']
        requirements = request.form['requirements']
        image = request.form['image']
        cost = request.form['cost']

        conn = pymysql.connect(host="localhost", user="root", password="", database="game_store")
        #     insert the records to the products tables
        cursor = conn.cursor()
        cursor.execute("insert into games(product_id,name,requirements,image,cost) values('{}','{}','{}','{}','{}')".format(product_id, name, requirements, image, cost))
        conn.commit()
        return render_template('add_products.html', msg_games="Product added successfully")
    else:
        return render_template('add_products.html')

@app.route('/add_tech', methods=['POST', 'GET'])
def add_tech():
    if request.method == 'POST':
        product_id = request.form['product_id']
        name = request.form['name']
        image = request.form['image']
        cost = request.form['cost']

        conn = pymysql.connect(host="localhost", user="root", password="", database="game_store")
        #     insert the records to the products tables
        cursor = conn.cursor()
        cursor.execute("insert into tech(product_id,name,image,cost) values('{}','{}','{}','{}')".format(product_id, name, image, cost))
        conn.commit()
        return render_template('add_products.html', msg_tech="Product added successfully")
    else:
        return render_template('add_products.html')

@app.route('/tournament_application', methods=['POST', 'GET'])
def tournament_application():
    conn = pymysql.connect(host="localhost", user="root", password="", database="game_store")
    cursor = conn.cursor()
    # execute the query using the cursor
    cursor.execute("select * from tournaments_lineup where game = 'Mortal kombat 11' order by points DESC")       
        # check for records    
    game1 = cursor.fetchall()

    cursor.execute("select * from tournaments_lineup where game = 'Injustice 2' order by points DESC")       
        # check for records    
    game2 = cursor.fetchall()

    cursor.execute("select * from tournaments_lineup where game = 'FIFA 21' order by points DESC")       
        # check for records    
    game3 = cursor.fetchall()

    cursor.execute("select * from tournament_upload")
    # check for records
    tournaments = cursor.fetchall()


    if request.method == 'POST':
        name = request.form['full_name']
        number = request.form['phone_number']
        email = request.form['email']
        game = request.form['GOC']
        conn = pymysql.connect(host="localhost", user="root", password="", database="game_store")
        #     insert the records to the Tournaments tables
        cursor = conn.cursor()
        cursor.execute("insert into tournaments(name,number,email,game) values (%s,%s,%s,%s)",
                        (name, number, email, game,))

        cursor.execute("insert into tournaments_lineup(name,number,email,game) values (%s,%s,%s,%s)",
                        (name, number, email, game,))
        conn.commit()
        

        return render_template('tournament_application.html', msg="Application submitted successfully", game1=game1, game2=game2, game3=game3,tournaments=tournaments)
    

    else:
        return render_template('tournament_application.html', game1=game1, game2=game2, game3=game3, tournaments=tournaments)


@app.route('/tournament_lineup', methods=['POST', 'GET'])
def tournament_lineup():

    # we first connect to local host and game_store database
    conn = pymysql.connect(host="localhost", user="root", password="", database="game_store")
    #     insert the records to the products tables
    cursor = conn.cursor()
    cursor.execute("select * from tournaments_lineup order by game" )
    g1 = cursor.fetchall()

    return render_template('tournaments_lineup.html', g1=g1)

@app.route('/tournament_history', methods=['POST', 'GET'])
def tournament_history():

    # we first connect to local host and game_store database
    conn = pymysql.connect(host="localhost", user="root", password="", database="game_store")
    #     insert the records to the products tables
    cursor = conn.cursor()
    cursor.execute("select * from tournaments order by game" )
    rows = cursor.fetchall()

    cursor.execute("select * from tournament_upload")
    uploads = cursor.fetchall()

    return render_template('tournaments_history.html', rows=rows, uploads=uploads)

@app.route('/tournament_search', methods=['POST', 'GET'])
def tournament_search():
    if request.method == 'POST':
        id = request.form['id_reg']

        conn = pymysql.connect(host="localhost", user="root", password="", database="game_store")
        #     insert the records to the products tables
        cursor = conn.cursor()
        cursor.execute("select * from tournaments where id like'{}' OR name like '{}' or date_time like'{}'".format(id,id,id))

        if cursor.rowcount == 0:
            return render_template('tournaments_history.html', msg='REG NUMBER/NAME/DATE DOES NOT EXIST')
        else:
            rows = cursor.fetchall()
            return render_template('tournaments_history.html', rows=rows)


    else:
        return render_template('tournaments_history.html')

from uuid import uuid4
def make_unique(string):
    ident = uuid4().__str__()[:8]
    return f"{ident}-{string}"

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

UPLOAD_FOLDER = 'static/tournaments_uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
app.config['MAX_CONTENT_LENGTH'] = 16 * 1000 * 1000

@app.route('/tournament_upload', methods=['GET', 'POST'])
def upload_file():
    # if check_admin():
        if request.method == 'POST':
            # check if the post request has the file part
            if 'file' not in request.files:
                flash('No file part',"warning")
                return redirect("/add_games")
            file = request.files['file']
            # If the user does not select a file, the browser submits an
            # empty file without a filename.
            if file.filename == '':
                flash('No selected file','warning')
                return redirect('/add_games')
            elif file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                unique_filename = make_unique(filename)
                print('here')
                tournament_name = request.form['tournament_name']
                tournament_date = request.form['tournament_date']
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], unique_filename))
                sql  = "insert into tournament_upload(name, pic, date) values(%s, %s, %s)"
                try:
                    connection = pymysql.connect(host='localhost', user='root', password='',database='game_store')
                    cursor = connection.cursor()
                    cursor.execute(sql, (tournament_name,unique_filename, tournament_date ))
                    connection.commit()
                    flash("Uploaded Successfully","success")
                    return redirect('/add_games')
                except:
                    flash("Upload Failed", "danger")
                    return redirect('/add_games')

            else:
                flash("Uploaded File Not Allowed", "warning")
                return redirect('/add_games')
        else:
            return redirect('/add_games')

@app.route('/delete/<id>', methods=['POST', 'GET'])
def delete(id):
    # we first connect to local host and game_store database
    conn = pymysql.connect(host="localhost", user="root", password="", database="game_store")
    #     insert the records to the products tables
    cursor = conn.cursor()
    cursor.execute("delete from tournaments_lineup where id = %s", id )
    conn.commit()
    return redirect('/tournament_lineup')

@app.route('/points/<id>', methods=['POST', 'GET'])
def points(id):
    # we first connect to local host and game_store database
    conn = pymysql.connect(host="localhost", user="root", password="", database="game_store")
    #     insert the records to the products tables
    cursor = conn.cursor()
    cursor.execute("select * from tournaments where id = %s", id )
    rows = cursor.fetchall()
    for row in rows:
        old_points = row[5]
        new_points = 1000 + old_points
        cursor.execute("update tournaments set points=%s where id = %s", (new_points,id) )
        cursor.execute("update tournaments_lineup set points=%s where id = %s", (new_points,id) )
        conn.commit()
        return redirect (url_for('.tournament_lineup'))


    
# mpesa intergration
import requests
import datetime
import base64
from requests.auth import HTTPBasicAuth

@app.route('/mpesa_payment', methods = ['POST','GET'])
def mpesa_payment():
    if 'username' in session:
        connection = pymysql.connect(host='localhost', user='root', password='', database='game_store')
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM clients where username = %s", (session['username']))
        # AFter executing the query above, get all rows
        number = cursor.fetchall()
        session['request'] = 'accept'

        if request.method == 'POST':
            phone = str (request.form['phone'])
            account = request.form['account']
            # amount = str(request.form['amount'])

            #GENERATING THE ACCESS TOKEN
            consumer_key = "0aDsNA5rkQiAFJY594KxPtDkAfyZp51s"
            consumer_secret = "b96yLzkGAP5Lt44j"

            api_URL = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials" #AUTH URL
            r = requests.get(api_URL, auth=HTTPBasicAuth(consumer_key, consumer_secret))

            data = r.json()
            access_token = "Bearer" + ' ' + data['access_token']

            #  GETTING THE PASSWORD
            timestamp = datetime.datetime.today().strftime('%Y%m%d%H%M%S')
            passkey = 'bfb279f9aa9bdbcf158e97dd71a467cd2e0c893059b10f78e6b72ada1ed2c919'
            business_short_code = "174379"
            data = business_short_code + passkey + timestamp
            encoded = base64.b64encode(data.encode())
            password = encoded.decode('utf-8')


            # BODY OR PAYLOAD
            payload = {
                "BusinessShortCode": "174379",
                "Password": "{}".format(password),
                "Timestamp": "{}".format(timestamp),
                "TransactionType": "CustomerPayBillOnline",
                "Amount": "1", #use 1 when testing
                "PartyA": phone, #phone number that is paying
                "PartyB": "174379", #paybill number
                "PhoneNumber": phone, #phone number that is paying
                "CallBackURL": "https://nairobichoralfest.co.ke/booking/call.php",
                "AccountReference": account,
                "TransactionDesc": "account"
            }

            # POPULATING THE HTTP HEADER
            headers = {
                "Authorization": access_token,
                "Content-Type": "application/json"
            }

            url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest" #C2B URL

            response = requests.post(url, json=payload, headers=headers)

            print (response.text)
            session.pop('request', None)
            return render_template('mpesa_payment.html', msg = 'Please complete payment on your phone ')
        else:
            return render_template('mpesa_payment.html', number=number)
    else:
        session['page'] = 'mpesa'
        return redirect('/users_login')

@app.route('/logout')
def logout():
    # the process below simply checks if the cart item is in session and if so, empties the cart upon a user logging out in the middle of shopping
    if 'cart_item' in session:
        for key, value in session['cart_item'].items():
            ordercode =  session['cart_item'][key]['ordercode']
            id = session['cart_item'][key]['product_id']
            quantity =  session['cart_item'][key]['quantity']
            for item in session['cart_item'].items():
                if item[0] == ordercode:
                    conn = pymysql.connect(host="localhost", user="root", password="", database="game_store")
                    cursor = conn.cursor()
                    cursor.execute("select * from games where product_id = '{}'".format(id))
                    if cursor.rowcount == 1:
                        rows = cursor.fetchall()
                        for row in rows:
                            stock = row[5]
                            new_stock = stock + int(quantity)
                            cursor.execute("update games set quantity = %s where product_id = %s", (new_stock, id))
                            conn.commit()
                    else:
                        cursor.execute("select * from tech where product_id = '{}'".format(id))
                        rows = cursor.fetchall()
                        for row in rows:
                            stock = row[4]
                            new_stock = stock + int(quantity)
                            cursor.execute("update tech set quantity = %s where product_id = %s", (new_stock, id))
                            conn.commit()
        # after the cart is emptied all the below sessions are cleared and the user is logged out
        session.pop('username',None)
        session.pop('page',None)
        session.pop('cart_item', None)
        session.pop('all_total_quantity', None)
        session.pop('all_total_price', None)
        session.pop('page', None)
        return redirect('/users_login')
    # if the cart item is not in session, the sessions are cleared and the user is logged out
    else:
        session.pop('username', None)
        session.pop('page', None)
        session.pop('cart_item', None)
        session.pop('all_total_quantity', None)
        session.pop('all_total_price', None)
        session.pop('page', None)
        return redirect('/users_login')

if __name__ == '__main__':
    app.secret_key = "Wdg@#$%89jMfh2879mT"
    app.run(debug=True, port=2059)