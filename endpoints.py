from flask import Flask, redirect, url_for, render_template, request, session, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
import json
from shoppingcart import ShoppingCart

app = Flask(__name__)
app.secret_key = "secret_key"
app.permanent_session_lifetime = timedelta(seconds=15)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///user.sqlite3"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    phone = db.Column(db.String(50))
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(50))
    date_joined = db.Column(db.Date, default=datetime.utcnow)
    shopping_cart = db.Column(db.String())

    def __init__(self, first_name, last_name, phone, email, password):
        self.first_name = first_name
        self.last_name = last_name
        self.phone = phone
        self.email = email
        self.password = password

shopping_cart = ShoppingCart()

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/signin", methods=["GET", "POST"])
def signin():
    if request.method == "POST":
        session.permanent = True
        first_name = request.form["first_name"]
        last_name = request.form["last_name"]
        phone = request.form["phone"]
        email = request.form["email"]
        password = request.form["password"]
        session["email"] = email
        session["password"] = password

        found_user = User.query.filter_by(email=email).first()
        if found_user:
            flash("This email is already in use by an existing user, "
                  "please signin using a unique email / login using some other user in order to continue")
            return redirect(url_for("home"))
        else:
            user = User(first_name=first_name, last_name=last_name, phone=phone, email=email, password=password)
            db.session.add(user)
            db.session.commit()
            flash("Signed in successfully!")
            return redirect(url_for("menu"))
    else:
        return render_template("signin.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        session.permanent = True
        email = request.form["email"]
        password = request.form["password"]
        session["email"] = email
        session["password"] = password

        found_user = User.query.filter_by(email=email).first()
        if found_user:
            shopping_cart.shopping_dict = json.loads(found_user.shopping_cart) if found_user.shopping_cart else {}
        else:
            flash("User is not registered, please signin / login using some other user in order to continue.")
            return redirect(url_for("home"))

        flash("Logged in successfully!")
        return redirect(url_for("menu"))
    else:
        if "email" in session:
            flash("Already logged in.")
            return redirect(url_for("menu"))
        return render_template("login.html")

@app.route("/logout")
def logout():
    if "email" in session:
        email = session.pop("email")
        session.pop("password")
        flash(f"{email} have been logged out!")
    return redirect(url_for("login"))

@app.route("/edit")
def edit_profile():
    pass


@app.route("/menu")
def menu():
    if "email" in session:
        email = session["email"]
        products_num = shopping_cart.get_products_num()
        return render_template("menu.html", user=email, products_num=products_num)
    else:
        flash("You are not logged in!")
        return redirect(url_for("login"))

@app.route("/add", methods=["GET", "POST"])
def add_product():
    if "email" in session:
        if request.method == "POST":
            product_name = request.form.get("product_name")
            quantity = request.form.get("quantity")
            added = shopping_cart.add_product(product_name, int(quantity))
            if added:
                email = session["email"]
                found_user = User.query.filter_by(email=email).first()
                found_user.shopping_cart = json.dumps(shopping_cart.shopping_dict)
                db.session.commit()
                flash(f"{product_name} X {quantity} added to the shopping list.")
                return redirect(url_for("menu"))
            else:
                flash("Product already appears in the shopping list, you can update its quantity if necessary.")
                return redirect(url_for("update_product"))
        else:
            return render_template("add.html")
    else:
        flash("You are not logged in!")
        return redirect(url_for("login"))

@app.route("/update", methods=["GET", "POST"])
def update_product():
    if "email" in session:
        if request.method == "POST":
            product_name = request.form.get("product_name")
            quantity = request.form.get("quantity")
            total = shopping_cart.update_product(product_name, int(quantity))
            if total:
                email = session["email"]
                found_user = User.query.filter_by(email=email).first()
                found_user.shopping_cart = json.dumps(shopping_cart.shopping_dict)
                db.session.commit()
                flash(f"{product_name} X {total} in the shopping list.")
                return redirect(url_for("menu"))
            else:
                flash("Product does not appear in the shopping list, please add it first.")
                return redirect(url_for("add_product"))
        else:
            return render_template("update.html")
    else:
        flash("You are not logged in!")
        return redirect(url_for("login"))

@app.route("/remove", methods=["GET", "POST"])
def remove_product():
    if "email" in session:
        if request.method == "POST":
            product_name = request.form.get("product_name")
            quantity = request.form.get("quantity")
            removed = shopping_cart.remove_product(product_name, int(quantity))
            if removed:
                email = session["email"]
                found_user = User.query.filter_by(email=email).first()
                found_user.shopping_cart = json.dumps(shopping_cart.shopping_dict)
                db.session.commit()
                flash(f"{product_name} X {quantity} removed from the shopping list.")
                return redirect(url_for("menu"))
            else:
                flash(f"Product {product_name} does not appear in the shopping list!")
                return redirect(url_for("menu"))
        else:
            return render_template("remove.html")
    else:
        flash("You are not logged in!")
        return redirect(url_for("login"))

@app.route("/get")
def view_shopping_list():
    if "email" in session:
        col_titles_list = ["#", "Product", "Quantity"]
        row_vals_lists = [[product, quantity] for product, quantity in shopping_cart.shopping_dict.items()]
        return render_template("present_shopping_list.html", col_titles_list=col_titles_list,
                               row_vals_lists=row_vals_lists)
    else:
        flash("You are not logged in!")
        return redirect(url_for("login"))

@app.route("/view")
def view_users():
    return render_template("view.html", users=User.query.all())

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    # app.run(host="0.0.0.0")
    app.run()
